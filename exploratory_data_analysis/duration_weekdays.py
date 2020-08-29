# /usr/bin/env python3

import pandas as pd
from datetime import timedelta
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
                  Avg_Time_Rides, 
                  COUNT(Date) AS Num_Days, 
                  ROUND(AVG(Avg_Time_Rides), 2) AS Average 
             FROM (SELECT strftime("%Y-%m-%d", End_Date) AS Date, 
                          Bike_Id, 
                          COUNT(Rental_Id) AS Num_Rides, 
                          AVG(Duration) AS Avg_Time_Rides 
                     FROM Journeys 
                    WHERE strftime("%w", End_Date) NOT IN ("0", "6")
                      AND strftime("%Y", End_Date) = "2019"
                      AND julianday(End_Date) - julianday(Start_Date) < 1
                 GROUP BY Date, 
                          Bike_Id 
                   HAVING Avg_Time_Rides > 0 ) 
                 GROUP BY Bike_Id'''
cursor = con.execute(query)

journey_results = cursor.fetchall()
bike_df = pd.DataFrame(journey_results, columns=[
                       x[0] for x in cursor.description])

# histogram
fig, axes = plt.subplots(figsize=(8, 6))
axes.hist(bike_df['Average']/60, 80, range=[0, 42],
          edgecolor='k', color='dodgerblue')
avg_minutes = round(bike_df['Average'].mean()/60)
avg_ride_timedelta = str(timedelta(seconds=round(bike_df['Average'].mean())))
formatted_avg_ride = f'''{avg_ride_timedelta.split(':')[1]}m {avg_ride_timedelta.split(':')[2]}s'''
axes.vlines(avg_minutes, axes.yaxis.get_data_interval()[0], axes.yaxis.get_data_interval()[
            1], linestyles='--', color='k', label=f'''Average: {formatted_avg_ride}''')
axes.set_xlabel('Average bike ride duration per weekday (minutes)')
axes.set_ylabel('Counts')
axes.set_title('Histogram of average bike ride duration per weekday in 2019')
# plt.grid(linestyle=':')
print(f'Time elapsed: {time() - t0:.2f} seconds')
fig.tight_layout()
plt.legend(loc='best')
plt.show()
