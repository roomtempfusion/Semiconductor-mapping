import numpy as np
import pandas as pd
import json

df = pd.read_csv('patents_data_energy.csv')

df['adjusted_claims'] = df['patent_num_claims'] / df['patent_num_combined_citations']
df['adjusted_claims'].replace(np.inf, -1, inplace=True)
df['adjusted_claims'] = df['adjusted_claims'].apply(lambda x: x / max(df['adjusted_claims'].values))
df['adjusted_claims'] = df['adjusted_claims'].apply(lambda x: 1 if x < 0 else x)
df['patent_num_claims'] = df['patent_num_claims'].apply(lambda x: x / max(df['patent_num_claims'].values))
df['patent_num_combined_citations'] = (df['patent_num_combined_citations'].apply
                                       (lambda x: x / max(df['patent_num_combined_citations'].values)))
df['patent_num_cited_by_us_patents'] = (df['patent_num_cited_by_us_patents'].apply
                                        (lambda x: x / max(df['patent_num_cited_by_us_patents'].values)))
df['patent_processing_time'] = (df['patent_processing_time'].apply(lambda x: x / max(df['patent_processing_time'].values)))
df.to_csv('patents_value.csv', index=False)
