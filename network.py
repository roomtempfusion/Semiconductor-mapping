import pandas as pd
import json
from geopy.geocoders import Nominatim
from random import randint
geolocator = Nominatim(user_agent="my_geocoder")

with open('country_mapping.json', 'r') as file:
    country_dict = json.load(file)
with open('official_names.json', 'r') as file:
    official_dict = json.load(file)

def official_name(input_str):

    # Convert input string to uppercase for case-insensitive matching
    input_str_upper = input_str.upper()

    for abbreviation, full_name in official_dict.items():
        if input_str_upper == abbreviation.upper():
            return full_name
    return input_str


def replace_country_name(input_str):

    # Convert input string to uppercase for case-insensitive matching
    input_str_upper = input_str.upper()

    for abbreviation, full_name in country_dict.items():
        if input_str_upper == abbreviation.upper():
            return full_name
    return input_str


def get_coordinates(input_string):
    input_string = input_string.split(',')
    try:
        city = input_string[-2].strip()
    except:
        city = None
    try:
        country = official_name(replace_country_name(input_string[-1].strip()))
    except:
        country = None
    try:
        location = geolocator.geocode(f"{city}, {country}", timeout=1)
        print(location)
    except Exception:
        try:
            location = geolocator.geocode(f"{country}", timeout=1)
            print(location)
        except Exception:
            return [None, None, country]
    if location is not None:
        return [float(location.latitude), float(location.longitude), country]
    else:
        return [None, None, country]


def remove_institution(institutions_list, institution_to_remove):
    modified_list = institutions_list.copy()
    if institution_to_remove in modified_list:
        modified_list.remove(institution_to_remove)
    return modified_list


def affiliation_location(x):
    try:
        latitude, longitude, country = get_coordinates(x)
        return latitude, longitude, country
    except:
        return None, None, None


csv_path = 'data_processed.csv'

df = pd.read_csv(csv_path)
df['Author Affiliations'] = df['Author Affiliations'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
df['Author Affiliations'].fillna(value='', inplace=True)
df['Affiliated Institutions'] = df['Author Affiliations']

df.drop(columns=['Document Title', 'Authors', 'Publication Title', 'Publication Year', 'Abstract', 'ISSN', 'DOI',
                 'Funding Information', 'PDF Link', 'Article Citation Count', 'Reference Count',
                 'Online Date', 'Author Countries', 'Countries'], inplace=True)

df = df.explode('Author Affiliations')

df['Affiliated Institutions'] = df.apply(lambda row: [inst for inst in row['Affiliated Institutions'] if inst != row['Author Affiliations']], axis=1)

df[['Latitude', 'Longitude', 'Country']] = df['Author Affiliations'].apply(lambda x: pd.Series(affiliation_location(x)))

df.to_csv('coordinates.csv', index=False)


