import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import re
import textwrap

# Extract strings enclosed in single quotes using regular expression

# Example list of sets
csv_path = "C:\\Users\\hkdeb\\PycharmProjects\\ie5bot\\ieee.csv"

df = pd.read_csv(csv_path)


institution_sets_list = df['Affiliations']
institutions = []
#print(institution_sets_list)
#print(institution_sets_list[0].split("', '")[0].strip('{').strip('}'))
for element in institution_sets_list:
    matches = re.findall(r"'(.*?)'", element)

    result_list = list(set(matches))
    institutions.append(result_list)

#print(institutions)
G = nx.Graph()

for element in institutions:
    #print(element)
    G.add_nodes_from(element)
    for i in range(0, len(element) - 1):
        if len(element) > 1:
            G.add_edge(element[i], element[i+1])

#G.add_nodes_from([1,2,3,4,5])
#G.add_edge(1,2)
isolated_nodes = list(nx.isolates(G))
G.remove_nodes_from(isolated_nodes)
node_degrees = dict(G.degree())
#print(node_degrees)
# Determine the threshold for the top 10% of nodes
print(max(node_degrees.values()))
#threshold = int(0.8 * max(node_degrees.values()))
threshold = 4
# Keep only nodes with degree above the threshold
top_nodes = [node for node, degree in node_degrees.items() if degree >= threshold]
filtered_graph = G.subgraph(top_nodes)

# Set a larger figure size
plt.figure(figsize=(15, 15))

# Customize axis limits for a zoomed-out effect
plt.axis('off')  # Turn off axis
plt.xlim([-1.5, 1.5])
plt.ylim([-1.5, 1.5])
labels = {node: '\n'.join(textwrap.wrap(node, width=15)) for node in G.nodes}

# Draw the graph
pos = nx.spring_layout(G, k=5000)  # Adjust the 'k' parameter for node and edge spacing
nx.draw_networkx_nodes(G, pos, node_color="skyblue", node_size=10000)
nx.draw_networkx_edges(G, pos, edge_color="gray", width=2)
nx.draw_networkx_labels(G, pos, labels=labels,font_size=8, font_color="black", font_weight="bold")

# Show the plot
plt.show()
