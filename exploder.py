import pandas as pd
import re
import textwrap
import networkx as nx
import plotly.graph_objects as go
import json

#get csv
csv_path = "C:\\Users\\hkdeb\\PycharmProjects\\ie5bot\\network_country.csv"

df = pd.read_csv(csv_path)

df['Edges'] = df['Edges'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)

df = df.explode('Edges')
df = df.drop(df.columns[0], axis=1)
df.to_csv('exploded_network_edges.csv', index=False)
print(df)