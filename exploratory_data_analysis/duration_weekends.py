# /usr/bin/env python3

import pandas as pd
import numpy as np
from pathlib import Path
import os, sqlite3
import matplotlib.pyplot as plt
from time import time

t0 = time()
home  = os.environ['HOME']
data_dir = Path(home) / 'Programming/data/s2ds-project-data'

# connect to SQLite DB on laptop
flow_journey_db = data_dir / 'journey-data_2019-2020.db'
con = sqlite3.connect(flow_journey_db)
query = '''SELECT Bike_Id, 
                  Tot_Time_Rides, 
                  COUNT(Day) AS Num_Days, 
                  ROUND(AVG(Tot_Time_Rides), 2) AS Average 
             FROM (SELECT strftime("%Y-%m-%d", End_Date) AS Day, 
                          Bike_Id, 
                          COUNT(Rental_Id) AS Num_Rides, 
                          SUM(Duration) AS Tot_Time_Rides 
                     FROM Journeys 
                    WHERE strftime("%w", End_Date) IN ("0", "6") 
                 GROUP BY Day, 
                          Bike_Id 
                   HAVING Tot_Time_Rides > 0 ) 
                 GROUP BY Bike_Id'''
cursor = con.execute(query)

journey_results = cursor.fetchall()
bike_df = pd.DataFrame(journey_results, columns = [x[0] for x in cursor.description])

# histogram
fig, axes = plt.subplots(figsize=(8, 6))
axes.hist(bike_df['Average']/60, 80, range=[0, 260], edgecolor='k', color='dodgerblue')
avg_minutes = bike_df['Average'].median()/60
axes.vlines(avg_minutes, axes.yaxis.get_data_interval()[0], axes.yaxis.get_data_interval()[1], linestyles=':', label = f'Median: {avg_minutes:.1f} min')
axes.set_xlabel('Average bike ride duration on weekends (minutes)')
axes.set_ylabel('Counts')
axes.set_title('Histogram of average bike ride duration on weekends')
# plt.grid(linestyle=':')
print(f'Time elapsed: {time() - t0:.2f} seconds')
fig.tight_layout()
plt.legend(loc='best')
plt.show()
