import pandas as pd
import json

df = pd.read_csv('data_processed.csv')
df['Author Keywords'] = df['Author Keywords'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
df['Authors'] = df['Authors'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
df['Author Affiliations'] = df['Author Affiliations'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
df['IEEE Terms'] = df['IEEE Terms'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
df['Author Countries'] = df['Author Countries'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
df['Countries'] = df['Countries'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
df['Funding Information'] = df['Funding Information'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)


def flatten_column(column):
    flat_series = df[f'{column}'].explode()
    # Get unique values from the Series
    unique_values = flat_series.value_counts()
    # If you want the result as a list, convert the unique values to a list
    unique_values_list = unique_values.to_dict()
    print(unique_values_list)


flatten_column('Author Countries')
