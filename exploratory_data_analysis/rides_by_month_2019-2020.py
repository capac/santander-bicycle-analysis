# /usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import os, sqlite3

home = os.environ['HOME']
data_dir = Path(home) / r'Programming/data/s2ds-project-data'
con = sqlite3.connect(data_dir / 'journey-data_2019-2020.db')
years = ['2019', '2020']
values = [('Weekdays', 'NOT'), ('Weekends', '')]
results_df_list = []
for year in years:
    for value in values:
        query = ''' SELECT strftime("%m", End_Date) AS Month, 
                           COUNT(Rental_Id) AS '''+value[0]+'''_'''+year+'''
                      FROM journeys
                     WHERE strftime("%w", End_Date) '''+value[1]+''' IN ("0", "6")
                       AND strftime("%Y", End_Date) = "'''+year+'''"
                  GROUP BY Month'''
        query_results = (con.execute(query), con.execute(query).fetchall())
        # print(query_results[0].description, query_results[1])
        df = pd.DataFrame(query_results[1], columns=[x[0] for x in query_results[0].description])
        # print(df.head())
        results_df_list.append(df)

results_df = pd.concat(results_df_list, axis=1)
# results_df.rename(columns={'Month_2019':'Month'}, inplace=True)
results_df = results_df.iloc[:, [0,1,3,5,7]].fillna(0)
results_df['Month'] = results_df['Month'].replace({'01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May', '06': 'Jun', '07': 'Jul', '08': 'Aug', '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'})

# plot
fig, ax = plt.subplots(figsize=(8, 6))
columns = [['Weekends_2019', 'Weekdays_2019'], ['Weekends_2020', 'Weekdays_2020']]
colors = [['forestgreen', 'limegreen'], ['royalblue', 'dodgerblue']]
width = 0.35
widths = [-width, width]
df = results_df.iloc[0:5].copy()
df.loc[:, [c for col in columns for c in col]] = df[[c for col in columns for c in col]].divide(1e5)
# print(df)
for col, color, wd in zip(columns, colors, widths):
    ax.bar(np.arange(5) + wd/2, df[col[0]], width, label=col[0].replace('_', ' '), color=color[0], edgecolor='k')
    ax.bar(np.arange(5) + wd/2, df[col[1]], width, label=col[1].replace('_', ' '), color=color[1], edgecolor='k', bottom=df[col[0]])

ax.set_xticks(np.arange(5))
ax.set_xticklabels(df['Month'], fontsize=12)
ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('Total number of rides (in units of 100,000)', fontsize=12)
ax.set_title('Total number of rides per month', fontsize=14)
# ax.grid(linestyle=':')
ax.legend(loc='best')
plt.tight_layout()
plt.show()
