import pandas as pd
import json
import matplotlib.pyplot as plt
df = pd.read_csv('patents_value_uk_cleaned.csv')
# df['Author Keywords'] = df['Author Keywords'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
# df['Authors'] = df['Authors'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
# df['Author Affiliations'] = df['Author Affiliations'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
# df['IEEE Terms'] = df['IEEE Terms'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
# df['Author Countries'] = df['Author Countries'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
# df['Countries'] = df['Countries'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
# df['Funding Information'] = df['Funding Information'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
df['assignees'] = df['assignees'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
#df['inventor_countries'] = df['inventor_countries'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)

def flatten_column(column):
    flat_series = df[f'{column}'].explode()
    # Get unique values from the Series
    unique_values = flat_series.value_counts()
    # If you want the result as a list, convert the unique values to a list
    unique_values_list = unique_values.to_dict()
    return unique_values_list

flat = flatten_column('assignees')
df_out = pd.DataFrame(data=flat.items(), index=range(0, len(flat)))
df_out.columns = ['assignee', 'count']
df_out.to_csv('assignees.csv', index=False)