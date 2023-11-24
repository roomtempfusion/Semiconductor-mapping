import pandas as pd
import networkx as nx
import plotly.graph_objects as go
import json
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="my_geocoder")


def get_coordinates(input_string):
    input_string = input_string.split(',')

    city = input_string[-2].strip()
    country = input_string[-1].strip()
    try:
        location = geolocator.geocode(f"{city}, {country}", timeout=1)
    except Exception:
        return [None, None]
    print(location)
    if location is None:
        return [None, None]
    return [location.latitude, location.longitude]


def get_coordinates_modified(input_string):
    try:
        location = geolocator.geocode(input_string, timeout=1)
        if location is not None:
            print(location)
        return [location.latitude, location.longitude]
    except Exception:
        return get_coordinates(input_string)
#get csv
csv_path = "C:\\Users\\hkdeb\\PycharmProjects\\ie5bot\\ieeef1000raw.csv"

df = pd.read_csv(csv_path)


#convert json from csv into lists
df['Affiliations'] = df['Affiliations'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
institutions = df['Affiliations']


connections_dict = {}
instcheck = []
# Iterate over lists
for institutions_list in institutions:
    # Iterate over each institution in the list
    for institution in institutions_list:
        instcheck.append(institution)
        # Check if the institution is already a key in the dictionary
        if institution not in connections_dict:
            # If not, add it with an empty list as the value
            connections_dict[institution] = []

        # Add connections to other institutions in the same list
        connections_dict[institution].extend(
            other_inst for other_inst in institutions_list if other_inst != institution)

# Remove duplicates from the connection lists
connections_dict = {key: list(set(value) - {key}) for key, value in connections_dict.items()}

#print(max_connections)
df = pd.DataFrame(list(connections_dict.items()), columns=['Source', 'Target'])
df['Target'] = df['Target'].apply(lambda x: json.dumps(x) if isinstance(x, (list, set)) else x)
lat = []
long = []
for inst in df['Source']:
    coords = get_coordinates_modified(inst)
    lat.append(coords[0])
    long.append(coords[1])
df['Latitude'] = lat
df['Longitude'] = long

df = df.explode('Target')
df.to_csv('network_gephi1.csv')
df.columns = ['id', 'Target', 'Latitude', 'Longitude']
df.to_csv('network_gephi2_.csv')


