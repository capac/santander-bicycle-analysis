# /usr/bin/env python3

import pandas as pd
import numpy as np
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
                  COUNT(*) AS Count
              FROM Journeys
            WHERE strftime("%w", End_Date) NOT IN ("0", "6")
              AND strftime("%Y", End_Date) IN ("2019")
              AND julianday(End_Date) - julianday(Start_Date) < 1
          GROUP BY Bike_Id
            HAVING Count>1'''

cursor = con.execute(query)
journey_results = cursor.fetchall()

# pandas dataframe
bike_df = pd.DataFrame(journey_results, columns=[x[0] for x in cursor.description])

# histogram
fig, axes = plt.subplots(figsize=(8, 6))
axes.hist(bike_df['Count'], 80, range=[1, 1200], edgecolor='k', color='dodgerblue')
counts_rides = round(bike_df['Count'].median())
axes.vlines(counts_rides, axes.yaxis.get_data_interval()[0], axes.yaxis.get_data_interval()[1], linestyles='--', color='k', label=f'''Median: {counts_rides}''')
axes.set_xlabel('Number of rides per bike on weekdays')
axes.set_xticks(np.linspace(0, 1200, 13))
plt.setp(axes.get_xticklabels(), ha="right", rotation_mode="anchor", rotation=45)
axes.set_ylabel('Counts')
axes.set_title('Histogram of number of rides per bike on weekdays in 2019')
# plt.grid(linestyle=':')
plt.legend(loc='best')
print(f'Time elapsed: {time() - t0:.2f} seconds')
fig.tight_layout()
plt.show()
