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
cursor = con.execute('''SELECT Bike_Id, COUNT(Rental_Id) AS Num_Journeys, SUM(Duration) AS Tot_Time FROM journeys GROUP BY Bike_Id HAVING Tot_Time > 1200''')

journey_results = cursor.fetchall()
bike_df = pd.DataFrame(journey_results, columns = [x[0] for x in cursor.description])
# for col in ['End_Date', 'Start_Date']:
#     bike_df[col] = pd.to_datetime(bike_df[col], format=r'%Y-%m-%d %H:%M:%S%f', errors='raise', exact=False)

# print(bike_df.head(10))
# print(bike_df.sort_values(by='count', ascending=False)[:10])
# print(bike_df.isna().any())

# max_min_days = bike_df['End_Date'].max() - bike_df['Start_Date'].min()
# total_duration = max_min_days.total_seconds()/(24*3600)

# grouped_bikes_and_journeys = bike_df['Rental_Id'].groupby(bike_df['Bike_Id'])
# grouped_journeys_per_bikes_per_day = grouped_bikes_and_journeys.count()/total_duration

bike_df['Journeys_Time'] = bike_df['Tot_Time'].divide(bike_df['Num_Journeys'])/60

# print(np.argwhere(np.isnan(bike_df['Num_Journeys'].values)))

# gtr_df = grouped_journeys_per_bikes_per_day.loc[grouped_journeys_per_bikes_per_day >= 0.5]
# print(gtr_df.sort_values(ascending=False))

fig, axes = plt.subplots(figsize=(8, 6))
axes.hist(bike_df['Journeys_Time'], 60, alpha=0.8, range=[0, 60], edgecolor='k', color='red')
axes.set_xlabel('Duration per bike')
plt.grid(linestyle=':')
print(f'Time elapsed: {time() - t0:.2f} seconds')
fig.tight_layout()
plt.show()
