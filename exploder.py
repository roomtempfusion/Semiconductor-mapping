import pandas as pd
import re
import textwrap
import networkx as nx
import plotly.graph_objects as go
import json

#get csv
csv_path = "C:\\Users\\hkdeb\\PycharmProjects\\ie5bot\\network.csv"

df = pd.read_csv(csv_path)

df['Values'] = df['Values'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)

df = df.explode('Values')
df = df.drop(df.columns[0], axis=1)
df.to_csv('exploded_network.csv', index=False)
print(df)