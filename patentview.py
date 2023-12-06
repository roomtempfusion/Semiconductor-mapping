# PatentView > PATSTAT
# america wins again
# see https://patentsview.org/apis/api-endpoints/patents for query information and what data fields are available
# see https://patentsview.org/apis/api-query-language#field_list_format for comparison operators and formatting
import requests
import pandas as pd
import json
import sys
api_url = 'https://api.patentsview.org/patents/query'

abstract_search_term = 'memristor'
# add with '_and' to narrow down cross-domain keywords: {'_text_any': {'patent_title/abstract': 'semiconductor'}}
query = {'q': {'_or':
                   [{'_text_any': {'patent_abstract': f'{abstract_search_term}'}},
                    {'_text_any': {'patent_title': f'{abstract_search_term}'}}
                    ]},
         'f': ['patent_title', 'ipc_section', 'ipc_class','ipc_subclass', 'inventor_country','inventor_latitude',
               'inventor_longitude',
               'patent_abstract', 'patent_number'],
         'o': {'per_page': 10000}}

response = requests.post(api_url, json=query)

df = pd.DataFrame(response.json()['patents'])

# If no results, end program
if len(df) == 0:
    print('No results')
    sys.exit()

# IPC Code processing
df_expanded = df['IPCs'].apply(pd.Series)

# Add new columns with the original DataFrame and remove IPC columns
df = pd.concat([df, df_expanded], axis=1).drop('IPCs', axis=1)

# Rename columns
for i in range(0, len(df.columns.tolist())):
    if i in df.columns.tolist():
        df.rename(columns={i: f'IPC_{i+1}'}, inplace=True)
        df[f'IPC_{i+1}'] = df[f'IPC_{i+1}'].fillna({i: {} for i in df.index})

# Combine IPC code values
for name in df.columns.tolist():
    if 'IPC_' in name:
        df[name] = df[name].apply(
            lambda x: ''.join(x.values()) if x and all(v is not None for v in x.values()) else '')


filtered_columns = df.filter(like='IPC_', axis=1)


def remove_empty_strings(lst):
    return [value for value in lst if value != '']


# Combine values from filtered columns into a new column 'IPC Codes'
df['IPC Codes'] = filtered_columns.apply(lambda row: remove_empty_strings(row.tolist()), axis=1)

# Drop the original columns
df = df.drop(filtered_columns.columns, axis=1)

# Inventor processing
df_expanded = df['inventors'].apply(pd.Series)

# Concatenate the new columns with the original DataFrame
df = pd.concat([df, df_expanded], axis=1).drop('inventors', axis=1)

for i in range(0, len(df.columns.tolist())):
    if i in df.columns.tolist():
        df.rename(columns={i: f'Inventor {i+1}'}, inplace=True)
        df[f'Inventor {i+1}'] = df[f'Inventor {i+1}'].fillna({i: {} for i in df.index})


def extract_countries(row):
    countries = []
    #print(row)
    for col_data in row:
        if 'inventor_country' in col_data:
            country = col_data['inventor_country']
            if country:  # Check if the country is not empty
                countries.append(country)
    return countries


def extract_coords(row):
    coords_list = []
    for col_data in row:
        if 'inventor_latitude' in col_data:
            coords = [col_data['inventor_latitude'], col_data['inventor_longitude']]
            if coords:  # Check if the country is not empty
                coords_list.append(coords)
    return coords_list


# Apply the function to each row and create a new column 'inventor_countries'
df['inventor_countries'] = df.apply(lambda row: list(set(extract_countries(row))), axis=1)
df['coords'] = df.apply(lambda row: extract_coords(row), axis=1)

# Preserve list structure
df['inventor_countries'] = df['inventor_countries'].apply(lambda x: json.dumps(x) if isinstance(x, list) else x)
df['coords'] = df['coords'].apply(lambda x: json.dumps(x) if isinstance(x, list) else x)
df['IPC Codes'] = df['IPC Codes'].apply(lambda x: json.dumps(x) if isinstance(x, list) else x)

for name in df.columns.tolist():
    if 'Inventor' in name:
        #print(name)
        df.drop(name, axis=1, inplace=True)
abstract_search_term_safe = abstract_search_term.replace(' ', '_')
#print(abstract_search_term_safe)
df.to_csv(f'patents_data_{abstract_search_term_safe}.csv', index=False)
print(df)
