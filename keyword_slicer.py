import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

csv_path = "C:\\Users\\hkdeb\\PycharmProjects\\ie5bot\\ieeef1000raw.csv"
df = pd.read_csv(csv_path)

df['IEEE Keywords'] = df['IEEE Keywords'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
df['INSPEC Keywords'] = df['INSPEC Keywords'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
df['Author Keywords'] = df['Author Keywords'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)

keywords = ['Memristor', 'Architecture', 'Thermal processing', 'Power management', 'Parallel processing', 'TPUs',
            'Leading-edge node', 'Electronic design automation', 'Tensor processing unit']

new_df = pd.DataFrame(columns=df.columns)
counter = -1
for index, row in df.iterrows():
    counter += 1
    for key in keywords:
        if key.upper() in row[0].upper():
            new_df.loc[len(new_df.index)] = row
            continue
        if key.upper() in row[-4].upper():
            new_df.loc[len(new_df.index)] = row
            continue
    for element in row[-3]:
        for key in keywords:
            if key.upper() in element.upper():
                new_df.loc[len(new_df.index)] = row
                continue
    for element in row[-2]:
        for key in keywords:
            if key.upper() in element.upper():
                new_df.loc[len(new_df.index)] = row
                continue
    for element in row[-1]:
        for key in keywords:
            if key.upper() in element.upper():
                new_df.loc[len(new_df.index)] = row
                continue

new_df['Author(s)'] = new_df['Author(s)'].apply(lambda x: json.dumps(x) if isinstance(x, (list, set)) else x)
new_df['Countries'] = new_df['Countries'].apply(lambda x: json.dumps(x) if isinstance(x, (list, set)) else x)
new_df['Affiliations'] = new_df['Affiliations'].apply(lambda x: json.dumps(x) if isinstance(x, (list, set)) else x)
new_df['IEEE Keywords'] = new_df['IEEE Keywords'].apply(lambda x: json.dumps(x) if isinstance(x, (list, set)) else x)
new_df['INSPEC Keywords'] = new_df['INSPEC Keywords'].apply(lambda x: json.dumps(x) if isinstance(x, (list, set)) else x)
new_df['Author Keywords'] = new_df['Author Keywords'].apply(lambda x: json.dumps(x) if isinstance(x, (list, set)) else x)

new_df.drop_duplicates(subset=['Title']).to_csv('keyword_parsed.csv', index=False)
