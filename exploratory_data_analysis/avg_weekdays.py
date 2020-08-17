# /usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import os
import sqlite3

home = os.environ['HOME']
data_dir = Path(home) / r'Programming/data/s2ds-project-data'
con = sqlite3.connect(data_dir / 'journey-data_2019-2020.db')
query = '''SELECT Hour,
                  ROUND(AVG(Num_Rides), 2) AS Avg_Rides,
                  ROUND(AVG(Num_Bikes), 2) AS Avg_Bikes
             FROM (SELECT strftime("%Y-%m-%d", End_Date) AS Day,
                          strftime("%H", End_Date) AS Hour,
                          COUNT(Rental_Id) AS Num_Rides,
                          COUNT(DISTINCT(Bike_Id)) AS Num_Bikes
                     FROM Journeys
                    WHERE strftime("%w", End_Date) NOT IN ("0", "6")
                      AND strftime("%Y", End_Date) = "2019"
                 GROUP BY Day, Hour
                   HAVING Duration > 0)
                 GROUP BY Hour'''
cur = con.execute(query)
query_results = cur.fetchall()
results_df = pd.DataFrame(query_results, columns=[
                          x[0] for x in cur.description])

# plot
fig, ax = plt.subplots(figsize=(8, 6))
ax.bar(results_df['Hour'], results_df['Avg_Rides'],
       color='dodgerblue', edgecolor='k')
ax.set_xlabel('Hour')
ax.set_ylabel('Average number of rides')
ax.set_title('Average number of rides per hour on weekdays in 2019')
# ax.grid(linestyle=':')
fig.tight_layout()
plt.show()
