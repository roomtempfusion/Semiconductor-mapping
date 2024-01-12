import pandas as pd
import json
import matplotlib.pyplot as plt
df = pd.read_csv('patents_value.csv')
plt.hist(df['patent_value_sum'], bins=500, edgecolor='black')  # Adjust the number of bins as needed
# patent_num_claims	patent_num_combined_citations	patent_value_sum
# patent_num_cited_by_us_patents	patent_processing_time	foreign_priority

# Add labels and title
plt.xlabel('Sum Values')
plt.ylabel('Frequency')
plt.title('Distribution of Sum Values')

# Show the plot
plt.show()

