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
rides_results_df = results_df[['WeekEnd_Rides', 'WeekDay_Rides']].rename(columns={'WeekEnd_Rides': 'Weekend', 'WeekDay_Rides': 'Weekday'}, index={0: 'Jan', 1: 'Feb', 2: 'Mar', 3: 'Apr', 4: 'May', 5: 'Jun', 6: 'Jul', 7: 'Aug', 8: 'Sep', 9: 'Oct', 10: 'Nov', 11: 'Dec'})

rides_results_df['Monthly Weekday Ratio'] = rides_results_df.apply(lambda row: row['Weekday']/(row['Weekday'] + row['Weekend']), axis=1)
rides_results_df['Monthly Weekend Ratio'] = rides_results_df.apply(lambda row: row['Weekend']/(row['Weekday'] + row['Weekend']), axis=1)

# print(rides_results_df.head(24))

# plot
rides_results_df = rides_results_df[['Monthly Weekend Ratio', 'Monthly Weekday Ratio']]
ax = rides_results_df.plot(kind='bar', stacked=True, figsize=(8, 6), color=['limegreen', 'dodgerblue'], fontsize=12, edgecolor='k')
ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('Ratio', fontsize=12)
ax.set_title('Ratio of number of rides per weekday over weekend per month', fontsize=14)

# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), labels=['Weekend', 'Weekday'])
plt.tight_layout()
plt.show()
