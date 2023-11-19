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
get_coordinates('e, wzwz')
#get csv
csv_path = "C:\\Users\\hkdeb\\PycharmProjects\\ie5bot\\ieee_f500_raw.csv"

df = pd.read_csv(csv_path)


#convert json from csv into lists
raw_inst_strs = df['Affiliations']
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
new_dict = {}
#create dict with institutions that have a certain number of connections
connection_threshold = 3
num_connections_dict = {}
max_connections = 0
# for item in connections_dict.items():
#     if len(item[1]) >= connection_threshold:
#         new_dict[item[0]] = item[1]
#     num_connections_dict[item[0]] = len(item[1])
#     if len(item[1]) > max_connections:
#         max_connections = len(item[1])


#print(max_connections)
df = pd.DataFrame(list(connections_dict.items()), columns=['Nodes', 'Edges'])
df['Edges'] = df['Edges'].apply(lambda x: json.dumps(x) if isinstance(x, (list, set)) else x)
lat = []
long = []
for inst in df['Nodes']:
    lat.append(get_coordinates(inst)[0])
    long.append(get_coordinates(inst)[1])
df['Latitude'] = lat
df['Longitude'] = long
df.to_csv('network.csv')

G = nx.DiGraph()

# Add nodes and edges to the graph
for institution, related_institutions in new_dict.items():
    G.add_node(institution)
    G.add_edges_from([(institution, related_inst) for related_inst in related_institutions])

pos = nx.fruchterman_reingold_layout(G, k=50)

# Create edges trace

edge_trace = go.Scatter(
    x=[],
    y=[],
    line=dict(width=0.5, color='#888'),  # Set the width and color of edges
    hoverinfo='none',
    mode='lines')

for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_trace['x'] += tuple([x0, x1, None])
    edge_trace['y'] += tuple([y0, y1, None])

# Create nodes trace
node_trace = go.Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers',
    hoverinfo='text',
    marker=dict(
        color=[degree for degree in num_connections_dict.values()],
        size=10,
        cmin=0,
        cmax=max_connections,  # Set the maximum value for the color scale
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right',
            tickvals=list(range(max_connections + 1)),
            ticktext=list(range(max_connections + 1)),
            tickmode='array',  # Set tick mode to 'array'
            tickcolor='white',  # Set tick color
            ticklen=4,  # Set tick length
            tickformat='.2f',  # Set tick format for continuous scale
            ticks='outside'  # Set tick placement
        ),
        colorscale='YlGnBu'  # Set the desired colorscale
    )
)


for node, pos_value in pos.items():
    x, y = pos_value
    text_label = f"{node}\n| # of Connections: {num_connections_dict[node]}"
    node_trace['x'] += tuple([x])
    node_trace['y'] += tuple([y])
    node_trace['text'] += tuple([text_label])


# Update marker size and color based on node degrees
node_degrees = dict(G.degree())
node_trace['marker']['size'] = [3 * degree for degree in node_degrees.values()]
node_trace['marker']['color'] = [degree for degree in node_degrees.values()]

# Create figure
fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=0, l=0, r=0, t=0),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )

# Show the plot
fig.show()
