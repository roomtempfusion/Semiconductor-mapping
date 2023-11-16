import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import re
import textwrap
import scipy

# Example list of sets
csv_path = "C:\\Users\\hkdeb\\PycharmProjects\\ie5bot\\ieee_f300_raw.csv"

df = pd.read_csv(csv_path)

raw_inst_strs = df['Affiliations']
institutions = []
for element in raw_inst_strs:
    matches = re.findall(r"'(.*?)'", element)

    result_list = list(set(matches))
    institutions.append(result_list)

connections_dict = {}
instcheck = []
# Iterate over sets
for institution_set in institutions:
    # Convert the set to a list for easier iteration
    institutions_list = list(institution_set)

    # Iterate over each institution in the set
    for institution in institutions_list:
        instcheck.append(institution)
        # Check if the institution is already a key in the dictionary
        if institution not in connections_dict:
            # If not, add it with an empty list as the value
            connections_dict[institution] = []

        # Add connections to other institutions in the same set
        connections_dict[institution].extend(
            other_inst for other_inst in institutions_list if other_inst != institution)

# Remove duplicates from the connection lists
connections_dict = {key: list(set(value) - {key}) for key, value in connections_dict.items()}
new_dict = {}
num_connections_dict = {}
for item in connections_dict.items():
    if len(item[1]) >= 5:
        new_dict[item[0]] = item[1]
    num_connections_dict[item[0]] = len(item[1])
G = nx.DiGraph()
plt.figure(figsize=(15, 15))

# Add nodes and edges to the graph
for institution, related_institutions in new_dict.items():
    G.add_node(institution)
    G.add_edges_from([(institution, related_inst) for related_inst in related_institutions])

pos = nx.spring_layout(G, k=1000000)
labels = {node: '\n'.join(textwrap.wrap(node, width=15)) for node in G.nodes}
colormap = []
node_degrees = dict(G.degree())

for node, degree in node_degrees.items():
    colormap.append((1/(1+2*float(degree)), float(degree)*12/255, 0))


# Draw nodes, edges, and labels
nx.draw_networkx_nodes(G, pos, node_color=colormap, node_size=2000)
nx.draw_networkx_edges(G, pos, edge_color="black", width=2)
nx.draw_networkx_labels(G, pos, labels=labels,font_size=4, font_color="white", font_weight="bold")


plt.axis('off')  # Turn off axis
plt.xlim([-1.5, 1.5])
plt.ylim([-1.5, 1.5])

# Show the plot
plt.show()

