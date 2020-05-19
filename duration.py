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
query = '''SELECT Bike_Id, Tot_Time, COUNT(Num_Journeys) AS Count_Journeys, ROUND(1.0*Tot_Time/COUNT(DISTINCT(Day)), 2) AS Average FROM (SELECT strftime("%Y-%m-%d", End_Date) AS Day, Bike_Id, COUNT(Rental_Id) AS Num_Journeys, SUM(Duration) AS Tot_Time FROM Journeys GROUP BY Day, Bike_Id HAVING Tot_Time > 0) GROUP BY Bike_Id'''
# query = '''SELECT * FROM DurationBikeDay'''
cursor = con.execute(query)

journey_results = cursor.fetchall()
bike_df = pd.DataFrame(journey_results, columns = [x[0] for x in cursor.description])

# histogram
fig, axes = plt.subplots(figsize=(8, 6))
axes.hist(bike_df['Average'], 80, range=[0, 30], alpha=0.8, edgecolor='k', color='cornflowerblue')
axes.vlines(bike_df['Average'].mean(), axes.yaxis.get_data_interval()[0], axes.yaxis.get_data_interval()[1], linestyles=':')
axes.set_xlabel('Duration per bike (min)')
axes.set_xlabel('Average bike ride duration per day')
axes.set_ylabel('Counts')
axes.set_title('Histogram of average bike ride duration per day')
plt.grid(linestyle=':')
print(f'Time elapsed: {time() - t0:.2f} seconds')
fig.tight_layout()
plt.show()
