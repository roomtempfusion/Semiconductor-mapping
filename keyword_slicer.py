import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

csv_path = "patents_value.csv"
df = pd.read_csv(csv_path)
df.fillna('', inplace=True)

# df['IEEE Terms'] = df['IEEE Terms'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
# df['Author Keywords'] = df['Author Keywords'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
# df['Countries'] = df['Countries'].apply(lambda x: json.loads(x) if isinstance(x, str) and x.strip() else x)
df['inventor_countries'] = df['inventor_countries'].apply(lambda x: json.loads(x) if isinstance(x, str) and x.strip() else x)

# keywords = ['integrated circuit packaging', 'IC packaging', 'integrated packaging', "semiconductor device packaging"]
# keywords = ['Memristor', 'Architecture', 'Thermal processing', 'Power management', 'Parallel processing', 'TPUs',
#           'Leading-edge node', 'Electronic design automation', 'tensor processing unit']
# keywords = ['gallium', 'Gallium Nitride', 'Gallium Oxide', 'Silicon Carbide', 'GaN', 'Ga2O3', 'SiC', 'power amplifiers',
#             'power amplifier architectures', 'wide band gap semiconductors', 'power electronics',
#             'power semiconductor devices', 'photonic band gap', 'wide band gap', 'power semiconductor']

# keywords = ["Renewable energy", "Energy storage systems", "Power generation", "Smart grids", "Electrical transmission",
#             "Grid integration", "Battery technologies", "Photovoltaics", "Wind power"]
keywords = ['United Kingdom']
lower_keys = [key.lower() for key in keywords]
new_df = pd.DataFrame(columns=df.columns)


def key_searcher(row):
    for key in lower_keys:
        if key in row['Document Title'].lower():
            return True
        # if key in row['Abstract'].lower():
        #     return True
    lower_ieee = [key.lower() for key in row['IEEE Terms']]
    lower_author = [key.lower() for key in row['Author Keywords']]
    if set(lower_keys).intersection(set(lower_ieee)):
        return True
    if set(lower_keys).intersection(set(lower_author)):
        return True
    return False

def country_searcher(row):
    for key in keywords:
        if key in row['inventor_countries']:
            return True
    return False


mask = df.apply(country_searcher, axis=1)
df = df[mask]

# df['IEEE Terms'] = df['IEEE Terms'].apply(lambda x: json.dumps(x) if isinstance(x, list) else x)
# df['Author Keywords'] = df['Author Keywords'].apply(lambda x: json.dumps(x) if isinstance(x, list) else x)
# df['Countries'] = df['Countries'].apply(lambda x: json.dumps(x) if isinstance(x, list) else x)
df['inventor_countries'] = df['inventor_countries'].apply(lambda x: json.dumps(x) if isinstance(x, list) else x)

df.to_csv('patents_value_uk.csv', index=False)
