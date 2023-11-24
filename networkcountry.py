import pandas as pd
import networkx as nx
import plotly.graph_objects as go
import json
from geopy.geocoders import Nominatim

csv_path = "C:\\Users\\hkdeb\\PycharmProjects\\ie5bot\\network.csv"

geolocator = Nominatim(user_agent="my_geocoder")

df = pd.read_csv(csv_path)

country_iso_dict = {
    'Australia': 'AU',
    'Belgium': 'BE',
    'Finland': 'FI',
    'United States': 'US',
    'Canada': 'CA',
    'UAE': 'AE',
    'Lithuania': 'LT',
    'Mexico': 'MX',
    'Hungary': 'HU',
    'Taiwan': 'TW',
    'Ireland': 'IE',
    'Jordan': 'JO',
    'Saudi Arabia': 'SA',
    'Switzerland': 'CH',
    'China': 'CN',
    'Russia': 'RU',
    'Austria': 'AT',
    'Belarus': 'BY',
    'Argentina': 'AR',
    'India': 'IN',
    'Japan': 'JP',
    'Israel': 'IL',
    'Singapore': 'SG',
    'France': 'FR',
    'Hong Kong': 'HK',
    'Spain': 'ES',
    'Denmark': 'DK',
    'Georgia': 'GE',
    'Brazil': 'BR',
    'Greece': 'GR',
    'Germany': 'DE',
    'Turkey': 'TR',
    'Netherlands': 'NL',
    'United Kingdom': 'GB',
    'Czech Republic': 'CZ',
    'Iran': 'IR',
    'Italy': 'IT',
    'Sweden': 'SE',
    'South Korea': 'KR',
    'Ukraine': 'UA',
    'Poland': 'PL'
}

def replace_country_name(input_str):

    country_dict = {
        'US': 'United States',
        'USA': 'United States',
        'CN': 'China',
        'P. R. China': 'China',
        'R.O.C': 'Taiwan',
        'R.O.C.': 'Taiwan',
        'ROC': 'Taiwan',
        'TW': 'Taiwan',
        'U.K': 'United Kingdom',
        'U.K.': 'United Kingdom',
        'UK': 'United Kingdom',
        'JP': 'Japan',
        'Republic of Korea': 'South Korea',
        'Republic ofKorea': 'South Korea',
        'Korea': 'South Korea',
        'ROK': 'South Korea',
        'The Netherlands': 'Netherlands'
    }
    us_states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY',
                 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND',
                 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

    # Convert input string to uppercase for case-insensitive matching
    input_str_upper = input_str.upper()

    for state in us_states:
        if input_str_upper == state:
            return 'United States'

    for abbreviation, full_name in country_dict.items():
        if input_str_upper == abbreviation.upper():
            return full_name
    return input_str


def get_coordinates(input_string):
    country_codes = None
    for cname, code in country_iso_dict.items():
        #print(cname, code)
        if input_string == cname:
            input_string = code
            country_codes = code

    #print(country_codes)
    try:
        if country_codes is None:
            location = geolocator.geocode(input_string, timeout=1)
        else:
            location = geolocator.geocode(input_string, timeout=1, country_codes=country_codes)
    except Exception:
        print(None)
        return None
    if location is None:
        print(None)
        return [None, None]
    print(location)
    return [location.latitude, location.longitude]


country_list = []

for country in df['Nodes']:
    country_string = replace_country_name(country.split(', ')[-1])
    country_list.append(country_string)

df['Country'] = country_list

for index, row in df.iterrows():
    if pd.isnull(row['Latitude']):
        #print(row['Country'])
        coords = get_coordinates(row['Country'])
        df.at[index, 'Latitude'] = coords[0]
        df.at[index, 'Longitude'] = coords[1]
        #print(coords)
#print(set(df['Country'].values))
df.to_csv('network_country.csv', index=False)
