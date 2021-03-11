# /usr/bin/env python3

import pandas as pd
from pathlib import Path
import os
import sqlite3
import matplotlib.pyplot as plt
from time import time

t0 = time()
home = os.environ['HOME']
data_dir = Path(home) / 'Programming/data/s2ds-project-data'

# connect to SQLite DB on laptop
flow_journey_db = data_dir / 'journey-data_2019-2020.db'
con = sqlite3.connect(flow_journey_db)
query = '''SELECT Bike_Id,
                  ROUND(AVG(Num_Rides), 2) AS Avg_Num_Rides
             FROM (SELECT strftime("%Y-%m-%d", End_Date) AS Date,
                          Bike_Id,
                          COUNT(Rental_Id) AS Num_Rides,
                          AVG(Duration) AS Avg_Time_Rides
                     FROM Journeys
                    WHERE strftime("%w", End_Date) IN ("0", "6")
                      AND strftime("%Y", End_Date) = "2019"
                      AND julianday(End_Date) - julianday(Start_Date) < 1
                 GROUP BY Date,
                          Bike_Id
                   HAVING Avg_Time_Rides > 0)
         GROUP BY Bike_Id'''

cursor = con.execute(query)
journey_results = cursor.fetchall()

# pandas dataframe
bike_df = pd.DataFrame(journey_results, columns=[
                       x[0] for x in cursor.description])

# histogram
fig, axes = plt.subplots(figsize=(8, 6))
axes.hist(bike_df['Avg_Num_Rides'], 60, range=[2, 6],
          edgecolor='k', color='dodgerblue')
avg_num_ride = bike_df['Avg_Num_Rides'].mean()
axes.vlines(avg_num_ride, axes.yaxis.get_data_interval()[
            0], axes.yaxis.get_data_interval()[1], linestyles='--', color='k',
            label=f'Average: {avg_num_ride:.1f}')
axes.set_xlabel('Average number of rides per bike on weekends')
axes.set_ylabel('Counts')
axes.set_title(
    'Histogram of average number of rides per bike on weekends in 2019')
# plt.grid(linestyle=':')
print(f'Time elapsed: {time() - t0:.2f} seconds')
plt.legend(loc='best')
fig.tight_layout()
plt.show()
