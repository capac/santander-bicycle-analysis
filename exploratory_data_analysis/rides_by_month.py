# /usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import os, sqlite3

home = os.environ['HOME']
data_dir = Path(home) / r'Programming/data/s2ds-project-data'
con = sqlite3.connect(data_dir / 'FlowJourneyData.db')
query = ''' SELECT strftime("%m", End_Date) AS Month, 
                   COUNT(Rental_Id) AS Num_Rides
              FROM Journeys 
          GROUP BY Month'''
cur = con.execute(query)
query_results = cur.fetchall()
results_df = pd.DataFrame(query_results, columns=[x[0] for x in cur.description])

# plot
fig, ax = plt.subplots(figsize=(8, 6))
ax.bar(results_df['Month'], results_df['Num_Rides']/1e5, color='cornflowerblue', edgecolor='k', alpha=0.8)
ax.set_xlabel('Month')
ax.set_ylabel('Number of rides (in units of 100,000)')
ax.set_title('Number of rides per month')
ax.grid(linestyle=':')
fig.tight_layout()
plt.show()
