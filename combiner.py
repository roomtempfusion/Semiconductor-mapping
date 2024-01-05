import pandas as pd
import json
import matplotlib.pyplot as plt
# df1 = pd.read_csv('patents_data_photovoltaic.csv')
# df2 = pd.read_csv('patents_data_renewable_energy.csv')
# df3 = pd.read_csv('patents_data_wind_power.csv')
# df4 = pd.read_csv('patents_data_wind_turbine.csv')
#
# df = pd.concat([df1, df2, df3, df4], ignore_index=True)
# df.drop_duplicates(inplace=True)
# df.to_csv('patents_data_energy.csv', index=False)

# df1 = pd.read_csv('paper_counts.csv')
# df2 = pd.read_csv('patent_metric.csv')
#
# result_df = pd.merge(df1, df2, on='Countries', how='outer')
# result_df.to_csv('combined.csv', index=False)

df = pd.read_csv('combined.csv')
plt.scatter(df['Count'], df['patent_value_sum'])

# Label each point with the country name
for i, txt in enumerate(df['Countries']):
    plt.annotate(txt, (df['Count'][i], df['patent_value_sum'][i]))

# Add labels and title
plt.xlabel('IEEE Papers')
plt.ylabel('Total Patent Value')
plt.title('IEEE Papers vs. Total Patent Value by Country')

# Show the plot
plt.show()
