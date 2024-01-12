# Creates a csv with statistical information about patents and papers for each country
# Generates a scatter plot using the above statistical information
import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np
df = pd.read_csv('patents_value.csv')
df['inventor_countries'] = df['inventor_countries'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)

df_exploded = df.explode('inventor_countries')

# Group by 'countries' and calculate the sum of 'values'
df_metrics = df_exploded.groupby('inventor_countries')['patent_value_sum'].agg(list).reset_index()
df_metrics['Patent sum'] = df_metrics['patent_value_sum'].apply(lambda x: sum(x))
df_metrics['Patent mean'] = df_metrics['patent_value_sum'].apply(lambda x: np.mean(x))
df_metrics['Patent median'] = df_metrics['patent_value_sum'].apply(lambda x: np.median(x))
df_metrics['Patent variance'] = df_metrics['patent_value_sum'].apply(lambda x: np.var(x))
df_metrics.drop(columns=['patent_value_sum'], inplace=True)
df_metrics.rename(columns={'inventor_countries': 'Countries'}, inplace=True)

df_papers = pd.read_csv('keywords_parsed_energy.csv')
df_papers['Article Citation Count'].fillna(0, inplace=True)
df_papers['Countries'] = df_papers['Countries'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
df_papers = df_papers.explode('Countries', ignore_index=True)
df_papers = df_papers.groupby('Countries')['Article Citation Count'].agg(list).reset_index()
df_papers['# Papers'] = df_papers['Article Citation Count'].apply(lambda x: len(x))
df_papers['Paper sum'] = df_papers['Article Citation Count'].apply(lambda x: sum(x))
df_papers['Paper mean'] = df_papers['Article Citation Count'].apply(lambda x: np.mean(x))
df_papers['Paper median'] = df_papers['Article Citation Count'].apply(lambda x: np.median(x))
df_papers['Paper variance'] = df_papers['Article Citation Count'].apply(lambda x: np.var(x))
df_papers.drop('Article Citation Count', axis=1, inplace=True)
df_papers.to_csv('papers_by_country_energy.csv', index=False)

merged_df = pd.merge(df_papers, df_metrics, on='Countries')
merged_df.to_csv('papers_patents_merged_energy.csv', index=False)
# merged_df = merged_df[merged_df['Paper sum'] <= 1000]
merged_df = merged_df[merged_df['Patent sum'] <= 300]
# Optional normalization
# merged_df['Paper sum'] = merged_df['Paper sum'].apply(lambda x: x/max(merged_df['Paper sum']))
# merged_df['Patent sum'] = merged_df['Patent sum'].apply(lambda x: x/max(merged_df['Patent sum']))

# Plotting a scatter plot for 'Paper sum' and 'Patent sum'
plt.scatter(merged_df['Paper sum'], merged_df['Patent sum'])

# Add labels and title
plt.xlabel('Total Citations for Papers')
plt.ylabel('Total Patent Value')
plt.title('Papers v Patents for Energy')

# Label points with values from the 'Countries' column
for i, label in enumerate(merged_df['Countries']):
    plt.annotate(label, (merged_df['Paper sum'].iloc[i], merged_df['Patent sum'].iloc[i]), textcoords="offset points", xytext=(0,5), ha='center')

# Show the plot
plt.show()


