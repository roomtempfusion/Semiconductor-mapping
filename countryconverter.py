import pandas as pd
import json

file_path = 'official_names.json'
with open(file_path, 'r', encoding='cp1252') as file:
    # Load the JSON data into a dictionary
    official_names = json.load(file)
file_path2 = 'country_mapping.json'
with open(file_path2, 'r', encoding='cp1252') as file:
    # Load the JSON data into a dictionary
    country_mapping = json.load(file)

df = pd.read_excel('EURAFR countries.xlsx')

data = pd.read_csv('data_processed.csv')


def country_converter(input_str):
    input_str_upper = input_str.upper()

    for abbreviation, full_name in country_mapping.items():
        if input_str_upper == abbreviation.upper():
            return full_name
    return input_str

def official_name_converter(input_str):
    input_str_upper = input_str.upper()

    for abbreviation, full_name in official_names.items():
        if input_str_upper == abbreviation.upper():
            return full_name
    return input_str

# column_list = df.iloc[:, 0].tolist()
df = df.iloc[:, 0].apply(lambda x: official_name_converter(country_converter(x)))
countries_list = df.tolist()
countries_list[15] = 'Georgia'
def country_searcher(row, country):
    if country in row['Countries']:
        return True
    return False
def country_parser(df_to_search, country):
    mask = df_to_search.apply(lambda row: country_searcher(row, country), axis=1)
    df = df_to_search[mask]
    return df

data.fillna('', inplace=True)
for country in countries_list:
    country_parser(data, country).to_csv(f'C:\\Users\\hkdeb\\PycharmProjects\\ie5bot\\data\\{country}_papersdata.csv', index=False)
    print(country)
