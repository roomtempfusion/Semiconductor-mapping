import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

csv_path = "C:\\Users\\hkdeb\\PycharmProjects\\ie5bot\\data_processed.csv"
df = pd.read_csv(csv_path)

df['IEEE Terms'] = df['IEEE Terms'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
df['Author Keywords'] = df['Author Keywords'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)

keywords = ['integrated circuit packaging', 'IC packaging', 'integrated packaging', "semiconductor device packaging"]

new_df = pd.DataFrame(columns=df.columns)
counter = -1
for index, row in df.iterrows():
    for key in keywords:
        if key.upper() in str(row[0]).upper():
            new_df.loc[len(new_df.index)] = row
            continue
        if key.upper() in str(row[5]).upper():
            new_df.loc[len(new_df.index)] = row
            continue
    for element in row[-5]:
        for key in keywords:
            if key.upper() in element.upper():
                new_df.loc[len(new_df.index)] = row
                continue

    for element in row[-6]:
        for key in keywords:
            if key.upper() in element.upper():
                new_df.loc[len(new_df.index)] = row
                continue


df['IEEE Terms'] = df['IEEE Terms'].apply(lambda x: json.dumps(x) if isinstance(x, list) else x)
df['Author Keywords'] = df['Author Keywords'].apply(lambda x: json.dumps(x) if isinstance(x, list) else x)

new_df.drop_duplicates(subset=['Document Title']).to_csv('keyword_parsed.csv', index=False)
