# america wins again
# see https://patentsview.org/apis/api-endpoints/patents for query information and what data fields are available
# see https://patentsview.org/apis/api-query-language#field_list_format for comparison operators and formatting
import requests
import pandas as pd
import json
import sys
from scipy.stats.mstats import winsorize
import numpy as np
import matplotlib.pyplot as plt
from fuzzywuzzy import process

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

file_path = 'official_names.json'
with open(file_path, 'r', encoding='cp1252') as file:
    # Load the JSON data into a dictionary
    official_names = json.load(file)
file_path2 = 'country_mapping.json'
with open(file_path2, 'r', encoding='cp1252') as file:
    # Load the JSON data into a dictionary
    country_mapping = json.load(file)


# Define functions


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


def de_abbrev(input_str):
    # Convert country name to standardized name
    # Convert input string to uppercase for case-insensitive matching
    input_str_upper = input_str.upper()

    for abbreviation, full_name in country_dict.items():
        if input_str_upper == abbreviation.upper():
            return full_name
    return input_str


def abbreviator(input_str):
    # Convert country name to standardized name
    # Convert input string to uppercase for case-insensitive matching
    input_str_upper = input_str.upper()

    for abbreviation, full_name in country_dict.items():
        if input_str_upper == full_name.upper():
            return abbreviation
    return None


def extract_countries(row):
    # Pull countries out of raw data
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


def remove_empty_strings(lst):
    return [value for value in lst if value != '']

def csv_combiner(*args):
    # Takes in a list of csv files and combines them into one dataframe
    df_list = []
    for i in range(0, len(args)):
        locals()[f'df{i}'] = pd.read_csv(args[i])
        df_list.append(locals()[f'df{i}'])
    df_combined = pd.concat(df_list, ignore_index=True)
    df_combined.drop_duplicates(inplace=True)
    return df_combined


def combiner(df_list):
    # Takes in a list of dataframes and combines them into one dataframe file
    df_combined = pd.concat(df_list, ignore_index=True)
    df_combined.drop_duplicates(inplace=True)
    return df_combined


def get_query(country):
    # Query the API
    # add with '_and' to narrow down cross-domain keywords: {'_text_any': {'patent_title/abstract': 'semiconductor'}}
    query = {'q': {'_and': [
        # {'_or':
        #                [{'_text_any': {'patent_abstract': f'{abstract_search_term}'}},
        #                 {'_text_any': {'patent_title': f'{abstract_search_term}'}}
        #                 ]},
                           {'_or':
                       [{'_text_any': {'patent_abstract': 'semiconductor'}},
                        {'_text_any': {'patent_title': 'semiconductor'}}
                        ]
                             },
                            {'assignee_country':f'{country}'}
                            ]},
             'f': ['patent_title', 'ipc_section', 'ipc_class','ipc_subclass', 'inventor_country','inventor_latitude',
                   'inventor_longitude',
                   'patent_abstract', 'patent_number', 'patent_num_claims', 'patent_num_combined_citations',
                   'patent_num_cited_by_us_patents', 'patent_processing_time', 'patent_year', 'forprior_docnumber',
                   'assignee_organization', 'app_type'],
             'o': {'per_page': 10000}}

    response = requests.post(api_url, json=query)
    df = pd.DataFrame(response.json()['patents'])
    return df


def patent_processor(df):
    # Processes raw data from API

    # IPC Code processing
    df_expanded = df['IPCs'].apply(pd.Series)

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

    df.dropna(axis=0, how='all', inplace=True)
    # Apply the function to each row and create a new column 'inventor_countries'
    df['inventor_countries'] = df.apply(lambda row: list(set(extract_countries(row))), axis=1)
    df['inventor_countries'] = df['inventor_countries'].apply(lambda x: [de_abbrev(country) for country in x])

    # Preserve list structure
    df['inventor_countries'] = df['inventor_countries'].apply(lambda x: json.dumps(x) if isinstance(x, list) else x)

    for name in df.columns.tolist():
        if 'Inventor' in name:
            #print(name)
            df.drop(name, axis=1, inplace=True)

    # Assignee processing
    df['assignees'] = df['assignees'].apply(lambda x: [d['assignee_organization'] for d in x] if isinstance(x, list) else x)

    # Foreign Patent Processing

    df['foreign_priority'] = (df['foreign_priority'].apply
        (lambda x: sum(1 for d in x if d['forprior_docnumber'] is not None) if isinstance(x, list) else x))
    return df


def country_searcher(row, country):
    if country in row['inventor_countries']:
        return True
    return False


def country_parser(df_to_search, country):
    mask = df_to_search.apply(lambda row: country_searcher(row, country), axis=1)
    df = df_to_search[mask]
    return df


def str_to_int(df_input):
    df_input['patent_processing_time'] = df_input['patent_processing_time'].apply(lambda x: int(x))
    df_input['patent_num_claims'] = df_input['patent_num_claims'].apply(lambda x: int(x))
    df_input['patent_num_combined_citations'] = df_input['patent_num_combined_citations'].apply(lambda x: int(x))
    df_input['patent_num_cited_by_us_patents'] = df_input['patent_num_cited_by_us_patents'].apply(lambda x: int(x))
    df_input['foreign_priority'] = df_input['foreign_priority'].apply(lambda x: int(x))
    return df_input


def metric_winsorize(df_input):
    # Winsorize to account for outliers
    df_input['patent_num_claims'] = winsorize(df_input['patent_num_claims'], limits=[0.01, 0.01])
    df_input['patent_num_combined_citations'] = (
        winsorize(df_input['patent_num_combined_citations'], limits=[0.01, 0.01]))
    df_input['patent_num_cited_by_us_patents'] = (
        winsorize(df_input['patent_num_cited_by_us_patents'], limits=[0.01, 0.01]))
    df_input['patent_processing_time'] = winsorize(df_input['patent_processing_time'], limits=[0.01, 0.01])
    df_input['foreign_priority'] = winsorize(df_input['foreign_priority'], limits=[0.01, 0.01])
    return df_input


def metric_calculator(df):
    df['adjusted_claims'] = df['patent_num_claims'] / df['patent_num_combined_citations']
    df['adjusted_claims'].replace(np.inf, -1, inplace=True)
    df['adjusted_claims'] = df['adjusted_claims'].apply(lambda x: x / max(df['adjusted_claims'].values))
    df['adjusted_claims'] = df['adjusted_claims'].apply(lambda x: 1 if x < 0 else x)
    df['patent_num_claims'] = df['patent_num_claims'].apply(lambda x: x / max(df['patent_num_claims'].values))
    df['patent_num_combined_citations'] = (df['patent_num_combined_citations'].apply
                                           (lambda x: x / max(df['patent_num_combined_citations'].values)))
    df['patent_num_cited_by_us_patents'] = (df['patent_num_cited_by_us_patents'].apply
                                            (lambda x: x / max(df['patent_num_cited_by_us_patents'].values)))
    df['patent_processing_time'] = (
        df['patent_processing_time'].apply(lambda x: 1 - (x / max(df['patent_processing_time'].values))))
    df['foreign_priority'] = df['foreign_priority'].apply(lambda x: x / max(df['foreign_priority'].values))

    df['patent_value_sum'] = (df['patent_processing_time'] + df['patent_num_combined_citations']
                              + df['patent_num_cited_by_us_patents'] + df['adjusted_claims'] + df['foreign_priority'])
    return df


def value_dist(df_sums, column):
    # patent_num_claims	patent_num_combined_citations	patent_value_sum
    # patent_num_cited_by_us_patents	patent_processing_time	foreign_priority
    plt.hist(df_sums[column], bins=500, edgecolor='black')  # Adjust the number of bins as needed

    # Add labels and title
    plt.xlabel('Sum Values')
    plt.ylabel('Frequency')
    plt.title('Distribution of Sum Values')

    # Show the plot
    plt.show()


def similarity_ratio(query, choice):
    return process.extractOne(query, [choice])[1]


def duplicate_purger(df):
    indices_dropped = []
    for i, ivalue in df['patent_abstract'].items():
        print(i)
        if i in indices_dropped:
            continue
        for j, jvalue in df['patent_abstract'].items():
            ratio = similarity_ratio(ivalue, jvalue)
            if ratio > 90 and (i != j):
                df.drop(index=j, inplace=True)
                indices_dropped.append(j)
    return df


def single_query(country):
    # Retrieve a single query from the API
    # keyword = Term to search from API
    # year = earliest year to retrieve data from (optional)
    df_raw = get_query(country)
    print('Raw data retrieved')
    df = patent_processor(df_raw)
    print('Data processed')
    df_processed = metric_calculator(metric_winsorize(str_to_int(df)))
    print('Metrics calculated')
    # df_clean = duplicate_purger(df_processed)
    # print('Duplicates purged')
    keyword_safe = country.replace(' ', '_').replace('"', '')
    df_processed.apply(lambda x: json.dumps(x) if isinstance(x, (list, set)) else x)
    df_processed.to_csv(f'patents_data_{keyword_safe}.csv', index=False)
    return df_processed


def multiple_query(*args):
    # Retrieve multiple queries from the API
    # args = countries to search from API
    if isinstance(args[0], list):
        countries = args[0]
    else:
        countries = list(args)
    for keyword in countries:
        converted = de_abbrev(keyword)
        print(converted)
        df_raw = get_query(keyword)
        print(len(df_raw))
        if len(df_raw) == 0:
            continue
        df = patent_processor(df_raw)
        df_processed = metric_calculator(metric_winsorize(str_to_int(df)))
        df_processed = df_processed.apply(lambda x: json.dumps(x) if isinstance(x, (list, set)) else x)
        keyword_safe = converted.replace(' ', '_').replace('"', '').lower()
        df_processed.to_csv(f'C:\\Users\\hkdeb\\PycharmProjects\\ie5bot\\data\\{keyword_safe}_patentsdata.csv', index=False)
    return None

# To combine multiple already processed csv files - enter the file names as strings in the list below
# df_multiple = csv_combiner()


# To show plot of distribution of any metric (one of below)
# patent_num_claims	patent_num_combined_citations	patent_value_sum
# patent_num_cited_by_us_patents	patent_processing_time	foreign_priority
# value_dist(df_metrics, 'patent_value_sum')

countries_SCA= [
    "AF",  # Afghanistan
    "BD",  # Bangladesh
    "BT",  # Bhutan
    "IN",  # India
    "KZ",  # Kazakhstan
    "KG",  # Kyrgyzstan
    "MV",  # Maldives
    "NP",  # Nepal
    "PK",  # Pakistan
    "LK",  # Sri Lanka
    "TJ",  # Tajikistan
    "TM",  # Turkmenistan
    "UZ"   # Uzbekistan
]
countries_NEA = [
    "QA",  # Qatar
    "SA",  # Saudi Arabia
    "SY",  # Syria
    "TN",  # Tunisia
    "AE",  # United Arab Emirates
    "YE"   # Yemen
]
countries_WHA = [
    "AG",  # Antigua and Barbuda
    "AR",  # Argentina
    "BS",  # The Bahamas
    "BB",  # Barbados
    "BZ",  # Belize
    "BO",  # Bolivia
    "BR",  # Brazil
    "CA",  # Canada
    "CL",  # Chile
    "CO",  # Colombia
    "CR",  # Costa Rica
    "CU",  # Cuba
    "DM",  # Dominica
    "DO",  # Dominican Republic
    "EC",  # Ecuador
    "SV",  # El Salvador
    "GD",  # Grenada
    "GT",  # Guatemala
    "GY",  # Guyana
    "HT",  # Haiti
    "HN",  # Honduras
    "JM",  # Jamaica
    "MX",  # Mexico
    "NI",  # Nicaragua
    "PA",  # Panama
    "PY",  # Paraguay
    "PE",  # Peru
    "KN",  # Saint Kitts and Nevis
    "LC",  # Saint Lucia
    "VC",  # Saint Vincent and the Grenadines
    "SR",  # Suriname
    "TT",  # Trinidad and Tobago
    "UY",  # Uruguay
    "VE"   # Venezuela
]

multiple_query(countries_WHA)


