# PatentView > PATSTAT
# america wins again
# see https://patentsview.org/apis/api-endpoints/patents for query information and what data fields are available
# see https://patentsview.org/apis/api-query-language#field_list_format for comparison operators and formatting
import requests
import pandas as pd
import json
import sys
api_url = 'https://api.patentsview.org/patents/query'
country_dict = {
    'AF': 'Islamic Republic of Afghanistan',
    'AL': 'Republic of Albania',
    'DZ': 'People\'s Democratic Republic of Algeria',
    'AD': 'Principality of Andorra',
    'AO': 'Republic of Angola',
    'AM': 'Republic of Armenia',
    'AT': 'Republic of Austria',
    'AZ': 'Republic of Azerbaijan',
    'BH': 'Kingdom of Bahrain',
    'BY': 'Republic of Belarus',
    'BJ': 'Republic of Benin',
    'BT': 'Kingdom of Bhutan',
    'BO': 'Plurinational State of Bolivia',
    'BA': 'Republic of Bosnia and Herzegovina',
    'BW': 'Republic of Botswana',
    'BG': 'Republic of Bulgaria',
    'BF': 'Burkina Faso',
    'BI': 'Republic of Burundi',
    'KH': 'Kingdom of Cambodia',
    'CM': 'Republic of Cameroon',
    'CV': 'Republic of Cabo Verde',
    'CF': 'Central African Republic',
    'TD': 'Republic of Chad',
    'KM': 'Union of the Comoros',
    'CR': 'Republic of Costa Rica',
    'HR': 'Republic of Croatia',
    'CU': 'Republic of Cuba',
    'CY': 'Republic of Cyprus',
    'DJ': 'Republic of Djibouti',
    'DO': 'Dominican Republic',
    'EC': 'Republic of Ecuador',
    'SV': 'Republic of El Salvador',
    'GQ': 'Republic of Equatorial Guinea',
    'ER': 'State of Eritrea',
    'ET': 'Federal Democratic Republic of Ethiopia',
    'FJ': 'Republic of Fiji',
    'FI': 'Republic of Finland',
    'GA': 'Gabonese Republic',
    'GM': 'Republic of The Gambia',
    'GE': 'Georgia',
    'GH': 'Republic of Ghana',
    'GT': 'Republic of Guatemala',
    'GN': 'Republic of Guinea',
    'GW': 'Republic of Guinea-Bissau',
    'GY': 'Co-operative Republic of Guyana',
    'HT': 'Republic of Haiti',
    'HN': 'Republic of Honduras',
    'IS': 'Republic of Iceland',
    'ID': 'Republic of Indonesia',
    'IQ': 'Republic of Iraq',
    'JM': 'Jamaica',
    'JO': 'Hashemite Kingdom of Jordan',
    'KZ': 'Republic of Kazakhstan',
    'KE': 'Republic of Kenya',
    'KG': 'Kyrgyz Republic',
    'LA': 'Lao People\'s Democratic Republic',
    'LV': 'Republic of Latvia',
    'LS': 'Kingdom of Lesotho',
    'LR': 'Republic of Liberia',
    'LY': 'State of Libya',
    'LI': 'Principality of Liechtenstein',
    'LT': 'Republic of Lithuania',
    'LU': 'Grand Duchy of Luxembourg',
    'MK': 'Republic of North Macedonia',
    'MG': 'Republic of Madagascar',
    'MW': 'Republic of Malawi',
    'ML': 'Republic of Mali',
    'MT': 'Republic of Malta',
    'MR': 'Islamic Republic of Mauritania',
    'MU': 'Republic of Mauritius',
    'MD': 'Republic of Moldova',
    'MC': 'Principality of Monaco',
    'MN': 'Mongolia',
    'ME': 'Montenegro',
    'MA': 'Kingdom of Morocco',
    'MZ': 'Republic of Mozambique',
    'MM': 'Republic of the Union of Myanmar',
    'NA': 'Republic of Namibia',
    'NP': 'Federal Democratic Republic of Nepal',
    'NI': 'Republic of Nicaragua',
    'NE': 'Republic of Niger',
    'NG': 'Federal Republic of Nigeria',
    'PS': 'State of Palestine',
    'PA': 'Republic of Panama',
    'PY': 'Republic of Paraguay',
    'PE': 'Republic of Peru',
    'PH': 'Republic of the Philippines',
    'RO': 'Romania',
    'RW': 'Republic of Rwanda',
    'SN': 'Republic of Senegal',
    'RS': 'Republic of Serbia',
    'SC': 'Republic of Seychelles',
    'SL': 'Republic of Sierra Leone',
    'SK': 'Slovak Republic',
    'SI': 'Republic of Slovenia',
    'SO': 'Federal Republic of Somalia',
    'ZA': 'Republic of South Africa',
    'LK': 'Democratic Socialist Republic of Sri Lanka',
    'SD': 'Republic of the Sudan',
    'SR': 'Republic of Suriname',
    'SZ': 'Kingdom of Eswatini',
    'TJ': 'Republic of Tajikistan',
    'TZ': 'United Republic of Tanzania',
    'TH': 'Kingdom of Thailand',
    'TL': 'Democratic Republic of Timor-Leste',
    'TG': 'Togolese Republic',
    'TT': 'Republic of Trinidad and Tobago',
    'TN': 'Republic of Tunisia',
    'TM': 'Turkmenistan',
    'UG': 'Republic of Uganda',
    'UY': 'Oriental Republic of Uruguay',
    'UZ': 'Republic of Uzbekistan',
    'VE': 'Bolivarian Republic of Venezuela',
    'YE': 'Republic of Yemen',
    'ZM': 'Republic of Zambia',
    'ZW': 'Republic of Zimbabwe',
    'US': 'United States of America',
    'CN': "People's Republic of China",
    'TW': 'Taiwan',
    'DK': 'Kingdom of Denmark',
    'GB': 'United Kingdom',
    'IN': 'Republic of India',
    'AU': 'Commonwealth of Australia',
    'IR': 'Islamic Republic of Iran',
    'CA': 'Canada',
    'KR': 'Republic of Korea',
    'DE': 'Germany',
    'ES': 'Kingdom of Spain',
    'SG': 'Republic of Singapore',
    'JP': 'Japan',
    'MX': 'United Mexican States',
    'IT': 'Italy',
    'FR': 'France',
    'BD': "People's Republic of Bangladesh",
    'EG': 'Arab Republic of Egypt',
    'MY': 'Malaysia',
    'PT': 'Portuguese Republic',
    'AE': 'United Arab Emirates',
    'TR': 'Republic of Turkey',
    'SA': 'Kingdom of Saudi Arabia',
    'HK': 'Hong Kong',
    'BR': 'Federative Republic of Brazil',
    'PK': 'Islamic Republic of Pakistan',
    'BE': 'Kingdom of Belgium',
    'NL': 'Kingdom of the Netherlands',
    'IL': 'State of Israel',
    'HU': 'Hungary',
    'RU': 'Russian Federation',
    'CZ': 'Czech Republic',
    'SE': 'Kingdom of Sweden',
    'PL': 'Republic of Poland',
    'EE': 'Republic of Estonia',
    'CL': 'Republic of Chile',
    'QA': 'State of Qatar',
    'NZ': 'New Zealand',
    'VN': 'Socialist Republic of Vietnam',
    'CH': 'Swiss Confederation',
    'SY': 'Syrian Arab Republic',
    'CO': 'Republic of Colombia',
    'LB': 'Lebanese Republic',
    'UA': 'Ukraine',
    'GR': 'Hellenic Republic',
    'AR': 'Argentine Republic',
    'OM': 'Sultanate of Oman',
    'KW': 'State of Kuwait',
    'IE': 'Republic of Ireland',
    'NO': 'Kingdom of Norway'
}

abstract_search_term = '"wind turbine"'
#year = 2005
# add with '_and' to narrow down cross-domain keywords: {'_text_any': {'patent_title/abstract': 'semiconductor'}}
query = {'q': {'_and': [{'_or':
                   [{'_text_any': {'patent_abstract': f'{abstract_search_term}'}},
                    {'_text_any': {'patent_title': f'{abstract_search_term}'}}
                    ]},
                        {'_or':
                   [{'_text_any': {'patent_abstract': 'semiconductor'}},
                    {'_text_any': {'patent_title': 'semiconductor'}}
                    ]},
                        #{'patent_year': f'{year}'}
                        ]},
         'f': ['patent_title', 'ipc_section', 'ipc_class','ipc_subclass', 'inventor_country','inventor_latitude',
               'inventor_longitude',
               'patent_abstract', 'patent_number', 'patent_num_claims', 'patent_num_combined_citations',
               'patent_num_cited_by_us_patents', 'patent_processing_time', 'patent_year', 'forprior_docnumber',
               'assignee_organization'],
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

# Fill None w 0
df['patent_processing_time'].fillna(0, inplace=True)


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
    try:
        if row is not None:
            for col_data in row:
                if isinstance(col_data, dict) and 'inventor_country' in col_data:
                    country = col_data['inventor_country']
                    if country:  # Check if the country is not empty
                        countries.append(country)
    except:
        return None
    return countries


def extract_coords(row):
    coords_list = []
    for col_data in row:
        if isinstance(col_data, dict) and 'inventor_latitude' in col_data:
            coords = [col_data['inventor_latitude'], col_data['inventor_longitude']]
            if coords:  # Check if the country is not empty
                coords_list.append(coords)
    return coords_list


def country_name(input_str):

    # Convert input string to uppercase for case-insensitive matching
    input_str_upper = input_str.upper()

    for abbreviation, full_name in country_dict.items():
        if input_str_upper == abbreviation.upper():
            return full_name
    return input_str


df.dropna(axis=0, how='all', inplace=True)
# Apply the function to each row and create a new column 'inventor_countries'
df['inventor_countries'] = df.apply(lambda row: list(set(extract_countries(row))), axis=1)
df['inventor_countries'] = df['inventor_countries'].apply(lambda x: [country_name(country) for country in x])
df['coords'] = df.apply(lambda row: extract_coords(row), axis=1)

# Preserve list structure
df['inventor_countries'] = df['inventor_countries'].apply(lambda x: json.dumps(x) if isinstance(x, list) else x)
df['coords'] = df['coords'].apply(lambda x: json.dumps(x) if isinstance(x, list) else x)
df['IPC Codes'] = df['IPC Codes'].apply(lambda x: json.dumps(x) if isinstance(x, list) else x)

for name in df.columns.tolist():
    if 'Inventor' in name:
        #print(name)
        df.drop(name, axis=1, inplace=True)

# Assignee processing
df['assignees'] = df['assignees'].apply(lambda x: [d['assignee_organization'] for d in x] if isinstance(x, list) else x)
df['assignees'] = df['assignees'].apply(lambda x: json.dumps(x) if isinstance(x, list) else x)

# Foreign Patent Processing

df['foreign_priority'] = (df['foreign_priority'].apply
    (lambda x: sum(1 for d in x if d['forprior_docnumber'] is not None) if isinstance(x, list) else x))
abstract_search_term_safe = abstract_search_term.replace(' ', '_').replace('"', '')
#print(abstract_search_term_safe)
df.to_csv(f'patents_data_{abstract_search_term_safe}.csv', index=False)
print(df)
