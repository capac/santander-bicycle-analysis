# /usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import os, sqlite3

home = os.environ['HOME']
data_dir = Path(home) / r'Programming/data/s2ds-project-data'
con = sqlite3.connect(data_dir / 'FlowJourneyData.db')
query_wkday = ''' SELECT strftime("%m", End_Date) AS Month, 
                         COUNT(Rental_Id) AS WeekDay_Rides
                    FROM Journeys
                   WHERE strftime("%w", End_Date) NOT IN ("0", "6")
                GROUP BY Month'''
query_wkend = ''' SELECT strftime("%m", End_Date) AS Month, 
                         COUNT(Rental_Id) AS WeekEnd_Rides
                    FROM Journeys
                   WHERE strftime("%w", End_Date) IN ("0", "6")
                GROUP BY Month'''
query_results = [(con.execute(cur), con.execute(cur).fetchall()) for cur in [query_wkday, query_wkend]]
results_df_list = [pd.DataFrame(result[1], columns=[x[0] for x in result[0].description]) for result in query_results]
results_df = pd.concat(results_df_list, axis=1)

# plot
rides_results_df = results_df[['WeekEnd_Rides', 'WeekDay_Rides']].rename(columns={'WeekEnd_Rides': 'Weekend', 'WeekDay_Rides': 'Weekday'}, index={0: 'Jan', 1: 'Feb', 2: 'Mar', 3: 'Apr', 4: 'May', 5: 'Jun', 6: 'Jul', 7: 'Aug', 8: 'Sep', 9: 'Oct', 10: 'Nov', 11: 'Dec'})
rides_results_df = rides_results_df.divide(1e5)
ax = rides_results_df.plot(kind='bar', stacked=True, figsize=(8, 6), color=['limegreen', 'dodgerblue'], fontsize=12, edgecolor='k')
ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('Number of rides (in units of 100,000)', fontsize=12)
ax.set_title('Number of rides per month', fontsize=14)
# ax.grid(linestyle=':')
ax.legend(loc='best')
plt.tight_layout()
plt.show()
