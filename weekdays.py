import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import os
import sqlite3

home = os.environ['HOME']
data_dir = Path(home) / r'Programming/data/s2ds-project-data'
con = sqlite3.connect(data_dir / 'FlowJourneyData.db')
query = ''' SELECT strftime("%H", End_Date) AS Hour, 
                   COUNT(Rental_Id) AS Num_Rides
              FROM Journeys 
             WHERE strftime("%w", End_Date) NOT IN ("0", "6") 
          GROUP BY Hour'''
cur = con.execute(query)
query_results = cur.fetchall()
results_df = pd.DataFrame(query_results, columns=[
                          x[0] for x in cur.description])

# plot
fig, ax = plt.subplots(figsize=(8, 6))
ax.bar(results_df['Hour'], results_df['Num_Rides']/1e5,
       color='cornflowerblue', edgecolor='k', alpha=0.8)
ax.set_xlabel('Hours')
ax.set_ylabel('Number of rides (in units of 100,000)')
ax.set_title('Number of rides per hour on weekdays')
ax.grid(linestyle=':')
fig.tight_layout()
plt.show()
