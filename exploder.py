import pandas as pd
import json
from geopy.geocoders import Nominatim
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
    try:
        location = geolocator.geocode({'country': input_string}, timeout=1)
        print(location)
    except Exception:
        return [None, None]
    if location is not None:
        return [float(location.latitude), float(location.longitude)]
    else:
        return [None, None]


csv_path = "coordinates_fixed.csv"
counter = 0
df = pd.read_csv(csv_path)
df['Affiliated Institutions'] = df['Affiliated Institutions'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
for index, row in df.iterrows():
    if pd.isnull(row['Latitude']):
        counter += 1
        #coords = get_coordinates(row['Country'])
        #df.at[index, 'Latitude'] = coords[0]
        #df.at[index, 'Longitude'] = coords[1]

print(counter)
#df = df.explode('Affiliated Institutions')

#df.to_csv('exploded_inst_2.csv', index=False)
