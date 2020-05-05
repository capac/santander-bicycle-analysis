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

# pandas dataframe
bike_df = pd.DataFrame(journey_results, columns = [x[0] for x in cursor.description])
bike_df['Journeys_Time'] = bike_df['Num_Journeys'].divide(bike_df['Tot_Time']/(24*3600))

# histogram
fig, axes = plt.subplots(figsize=(8, 6))
axes.hist(bike_df['Journeys_Time'], 100, range=[0, 150], alpha=0.8, edgecolor='k', color='red')
axes.set_xlabel('Number of journeys per bike per day')
plt.grid(linestyle=':')
print(f'Time elapsed: {time() - t0:.2f} seconds')
fig.tight_layout()
plt.show()
