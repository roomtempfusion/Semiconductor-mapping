import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np
csv_path = "C:\\Users\\hkdeb\\PycharmProjects\\ie5bot\\ieeef1000raw.csv"

df = pd.read_csv(csv_path)

keywords = 'IEEE Keywords'

# keywords = 'INSPEC Keywords'

# keywords = 'Author Keywords'

df = df[['Title', keywords]]


#convert json from csv into lists
df[keywords] = df[keywords].apply(lambda x: json.loads(x) if isinstance(x, str) else x)

df = df.explode(keywords)

frequency_counts = df[keywords].value_counts()

df_counts = frequency_counts.reset_index()

# Rename the columns if desired
df_counts.columns = ['Keywords', 'Count']

df_counts_sorted = df_counts.sort_values(by='Count')

df_filtered = df_counts_sorted[df_counts_sorted['Count'] >= 25]
selected_keys = list(df_filtered['Keywords'])
print(selected_keys)
fig, ax = plt.subplots(figsize=(10, 8))
# print(df_filtered)
# # Plot the horizontal bar chart
plt.barh(df_filtered['Keywords'], df_filtered['Count'], height=0.6)
plt.xlabel('Count')
plt.ylabel('Keyword')
plt.title(f'Most Common {keywords}')
plt.subplots_adjust(left=0.25, bottom=0.1)
ax.tick_params(axis='y', labelsize=8)

plt.show()

df = df.explode([keywords])

new_df = df[df[keywords].isin(selected_keys)]

#print(new_df)
#new_df.to_csv('keywordstest.csv')