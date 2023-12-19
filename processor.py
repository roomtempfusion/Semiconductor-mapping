import pandas as pd
import json

df = pd.read_csv('data.csv')

df['Authors'] = df['Authors'].apply(lambda x: x.split('; ') if isinstance(x, str) else x)
df['Author Affiliations'] = df['Author Affiliations'].apply(lambda x: x.split('; ') if isinstance(x, str) else x)
df['Author Keywords'] = df['Author Keywords'].apply(lambda x: x.split(';') if isinstance(x, str) else x)
df['IEEE Terms'] = df['IEEE Terms'].apply(lambda x: x.split(';') if isinstance(x, str) else x)
df.drop(columns=['Date Added To Xplore', 'Volume', 'Issue', 'Start Page', 'End Page', 'ISBNs', 'Mesh_Terms', 'License',
                 'Unnamed: 0', 'Patent Citation Count', 'Issue Date','Meeting Date','Publisher','Document Identifier'], inplace=True)

with open('country_mapping.json', 'r') as file:
    country_dict = json.load(file)
with open('official_names.json', 'r') as file:
    official_dict = json.load(file)

def replace_country_name(input_str):

    # Convert input string to uppercase for case-insensitive matching
    input_str_upper = input_str.upper()

    for abbreviation, full_name in country_dict.items():
        if input_str_upper == abbreviation.upper():
            return full_name
    return input_str

def official_name(input_str):

    # Convert input string to uppercase for case-insensitive matching
    input_str_upper = input_str.upper()

    for abbreviation, full_name in official_dict.items():
        if input_str_upper == abbreviation.upper():
            return full_name
    return input_str


def countries(list_of_affiliations):
    country_list = []
    for institution in list_of_affiliations:
        # print(institution)
        country = institution.split(', ')[-1]

        # check for abbreviations
        country = official_name(replace_country_name(country))

        country_list.append(country)
    return country_list


df['Author Countries'] = df['Author Affiliations'].apply(lambda x: countries(x) if isinstance(x, list) else '')
df['Author Affiliations'] = df['Author Affiliations'].apply(lambda x: list(set(x)) if isinstance(x, list) else '')
df['Funding Information'] = df['Funding Information'].apply(lambda x: x.split('; ') if isinstance(x, str) else x)
df = df.dropna(subset=['Author Countries', 'Authors', 'Author Affiliations'])
df['IEEE Terms'] = df['IEEE Terms'].fillna(value='z')
df['Author Keywords'] = df['Author Keywords'].fillna(value='z')
df['IEEE Terms'] = df['IEEE Terms'].apply(lambda x: [] if x == 'z' else x)
df['Author Keywords'] = df['Author Keywords'].apply(lambda x: [] if x == 'z' else x)


df = df[df['Author Countries'].apply(lambda x: x != ['NA'] if isinstance(x, list) else True)]
df = df[df['Author Countries'].apply(lambda x: x != [''] if isinstance(x, list) else True)]

value_to_remove = 'NA'  # Replace with the actual value you want to remove

# Use apply and lambda to remove the specified value from each list
df['Author Countries'] = df['Author Countries'].apply(lambda x: [item for item in x if item != value_to_remove])

# If you want to remove lists that become empty after removing the value, you can use:
df['Author Countries'] = df['Author Countries'].apply(lambda x: x if x else None)
df['Countries'] = df['Author Countries'].apply(lambda x: list(set(x)) if x else None)

df['Author Keywords'].fillna('', inplace=True)
df['IEEE Terms'].fillna('', inplace=True)

df['Author Keywords'] = df['Author Keywords'].apply(lambda x: json.dumps(x) if isinstance(x, list) else x)
df['Authors'] = df['Authors'].apply(lambda x: json.dumps(x) if isinstance(x, list) else x)
df['Author Affiliations'] = df['Author Affiliations'].apply(lambda x: json.dumps(x) if isinstance(x, list) else x)
df['IEEE Terms'] = df['IEEE Terms'].apply(lambda x: json.dumps(x) if isinstance(x, list) else x)
df['Author Countries'] = df['Author Countries'].apply(lambda x: json.dumps(x) if isinstance(x, list) else x)
df['Countries'] = df['Countries'].apply(lambda x: json.dumps(x) if isinstance(x, list) else x)
df['Funding Information'] = df['Funding Information'].apply(lambda x: json.dumps(x) if isinstance(x, list) else x)

df.to_csv('data_processed.csv', index=False)
