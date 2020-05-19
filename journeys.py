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
query = '''SELECT Bike_Id, SUM(Num_Rides) AS Tot_Num_Rides, COUNT(DISTINCT(Day)) AS Count_Journeys, ROUND(1.0*SUM(Num_Rides)/COUNT(DISTINCT(Day)), 2) AS Average FROM (SELECT strftime("%Y-%m-%d", End_Date) AS Day, Bike_Id, COUNT(Rental_Id) AS Num_Rides, SUM(Duration) AS Tot_Time FROM Journeys GROUP BY Day, Bike_Id HAVING Tot_Time > 0) GROUP BY Bike_Id'''
# query = '''SELECT Bike_Id, Tot_Num_Rides, Count_Journeys, Average FROM JourneysBikeDay'''
cursor = con.execute(query)
journey_results = cursor.fetchall()

# pandas dataframe
bike_df = pd.DataFrame(journey_results, columns = [x[0] for x in cursor.description])
# print(bike_df.head(20))

# histogram
fig, axes = plt.subplots(figsize=(8, 6))
axes.hist(bike_df['Average'], 60, range=[2, 6], alpha=0.8, edgecolor='k', color='cornflowerblue')
axes.vlines(bike_df['Average'].mean(), axes.yaxis.get_data_interval()[0], axes.yaxis.get_data_interval()[1], linestyles=':')
axes.set_xlabel('Average number of journeys per bike per day')
axes.set_ylabel('Counts')
axes.set_title('Histogram of average number of journeys per bike per day')
plt.grid(linestyle=':')
print(f'Time elapsed: {time() - t0:.2f} seconds')
fig.tight_layout()
plt.show()
