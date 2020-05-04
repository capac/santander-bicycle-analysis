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
flow_journey_db = data_dir / 'FlowJourneyData.db'
con = sqlite3.connect(flow_journey_db)
cursor = con.execute('''SELECT Bike_Id, COUNT(Rental_Id) AS Num_Journeys, SUM(Duration) AS Tot_Time FROM journeys GROUP BY Bike_Id HAVING Tot_Time > 0''')

journey_results = cursor.fetchall()
bike_df = pd.DataFrame(journey_results, columns = [x[0] for x in cursor.description])
# for col in ['End_Date', 'Start_Date']:
#     bike_df[col] = pd.to_datetime(bike_df[col], format=r'%Y-%m-%d %H:%M:%S%f', errors='raise', exact=False)

# print(bike_df.head(10))
# print(bike_df.sort_values(by='Tot_Time', ascending=False)[-10:])
# print(bike_df.isna().any())

# grouped_bikes_and_journeys = bike_df['Rental_Id'].groupby(bike_df['Bike_Id'])
# grouped_journeys_per_bikes_per_day = grouped_bikes_and_journeys.count()/total_duration

bike_df['Journeys_Time'] = (3600*24)*bike_df['Num_Journeys'].divide(bike_df['Tot_Time'])

# print(np.argwhere(np.isnan(bike_df['Num_Journeys'].values)))

fig, axes = plt.subplots(figsize=(8, 6))
axes.hist(bike_df['Journeys_Time'], 60, range=[0, 150], alpha=0.8, edgecolor='k', color='red')
axes.set_xlabel('Number of Journeys per bike per day')
plt.grid(linestyle=':')
print(f'Time elapsed: {time() - t0:.2f} seconds')
fig.tight_layout()
plt.show()
