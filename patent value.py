import numpy as np
import pandas as pd
import json
from scipy.stats.mstats import winsorize

df = pd.read_csv('patents_data_energy.csv')

# Winsorize to account for outliers

df['patent_num_claims'] = winsorize(df['patent_num_claims'], limits=[0.01, 0.01])
df['patent_num_combined_citations'] = winsorize(df['patent_num_combined_citations'], limits=[0.01, 0.01])
df['patent_num_cited_by_us_patents'] = winsorize(df['patent_num_cited_by_us_patents'], limits=[0.01, 0.01])
df['patent_processing_time'] = winsorize(df['patent_processing_time'], limits=[0.01, 0.01])
df['foreign_priority'] = winsorize(df['foreign_priority'], limits=[0.01, 0.01])

# Calculate metrics

df['adjusted_claims'] = df['patent_num_claims'] / df['patent_num_combined_citations']
df['adjusted_claims'].replace(np.inf, -1, inplace=True)
df['adjusted_claims'] = df['adjusted_claims'].apply(lambda x: x / max(df['adjusted_claims'].values))
df['adjusted_claims'] = df['adjusted_claims'].apply(lambda x: 1 if x < 0 else x)
df['patent_num_claims'] = df['patent_num_claims'].apply(lambda x: x / max(df['patent_num_claims'].values))
df['patent_num_combined_citations'] = (df['patent_num_combined_citations'].apply
                                       (lambda x: x / max(df['patent_num_combined_citations'].values)))
df['patent_num_cited_by_us_patents'] = (df['patent_num_cited_by_us_patents'].apply
                                        (lambda x: x / max(df['patent_num_cited_by_us_patents'].values)))
df['patent_processing_time'] = (df['patent_processing_time'].apply(lambda x: 1 - (x / max(df['patent_processing_time'].values))))
df['foreign_priority'] = df['foreign_priority'].apply(lambda x: x / max(df['foreign_priority'].values))


df['patent_value_sum'] = (df['patent_processing_time'] + df['patent_num_combined_citations']
                      + df['patent_num_cited_by_us_patents'] + df['adjusted_claims'] + df['foreign_priority'])

df.to_csv('patents_value.csv', index=False)


