import pandas as pd
import json
import matplotlib.pyplot as plt
df = pd.read_csv('keywords_parsed_energy.csv')
# df['Author Keywords'] = df['Author Keywords'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
# df['Authors'] = df['Authors'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
# df['Author Affiliations'] = df['Author Affiliations'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
# df['IEEE Terms'] = df['IEEE Terms'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
# df['Author Countries'] = df['Author Countries'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
df['Countries'] = df['Countries'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
# df['Funding Information'] = df['Funding Information'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)

#df['inventor_countries'] = df['inventor_countries'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)

def flatten_column(column):
    flat_series = df[f'{column}'].explode()
    # Get unique values from the Series
    unique_values = flat_series.value_counts()
    # If you want the result as a list, convert the unique values to a list
    unique_values_list = unique_values.to_dict()
    return unique_values_list
data = flatten_column('Countries')

df = pd.DataFrame(list(data.items()), columns=['Countries', 'Count'])
df.to_csv('paper_counts.csv', index=False)
print(df)
# e = flatten_column('IEEE Terms').to_frame()
# e.to_csv('e.csv')
# filtered_dict = {key: value for key, value in e.items() if value >= 5}
# plt.barh(list(filtered_dict.keys()), list(filtered_dict.values()))
# plt.xlabel('Number of Citations')
# plt.ylabel('Countries')
# plt.title('Total Number of IEEE Citations by Country')
# plt.subplots_adjust(left=0.3)  # Adjust left margin to make room for country names
# plt.show()
