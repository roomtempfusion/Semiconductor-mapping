import numpy as np
import pandas as pd
import json
from scipy.stats.mstats import winsorize


df = pd.read_csv('patents_value.csv')
df['inventor_countries'] = df['inventor_countries'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)


df = df.explode('inventor_countries')
sum_df = df.groupby('inventor_countries')['patent_value_sum'].sum().reset_index()
sum_df = sum_df.sort_values(by='patent_value_sum', ascending=False).reset_index(drop=True)
sum_df.rename(columns={'inventor_countries': 'Countries'}, inplace=True)
sum_df.to_csv('patent_metric.csv', index=False)
print(sum_df)