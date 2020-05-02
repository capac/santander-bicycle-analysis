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
cursor = con.execute('''SELECT * FROM journeys''')
journey_results = cursor.fetchall()
bike_df = pd.DataFrame(journey_results, columns = [x[0] for x in cursor.description])
for col in ['End_Date', 'Start_Date']:
    bike_df[col] = pd.to_datetime(bike_df[col], format=r'%Y-%m-%d %H:%M:%S%f', errors='raise', exact=False)

max_min_days = bike_df['End_Date'].max() - bike_df['Start_Date'].min()
total_duration = max_min_days.total_seconds()/(24*3600)

grouped_bikes_journeys_per_day = bike_df.groupby('Bike_Id')['Bike_Id'].count()/(total_duration)

fig, axes = plt.subplots(figsize=(8, 6))
axes.hist(grouped_bikes_journeys_per_day, 30, alpha=0.8, edgecolor='k', color='firebrick')
axes.set_xlabel('Number of journeys per bike per day')
plt.grid(linestyle=':')
print(f'Time elapsed: {time() - t0:.2f} seconds')
fig.tight_layout()
plt.show()
