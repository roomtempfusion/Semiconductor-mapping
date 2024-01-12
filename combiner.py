# Combines the data from the four csv files into one csv file

import pandas as pd
import json
import matplotlib.pyplot as plt
df1 = pd.read_csv('patents_data_photovoltaic.csv')
df2 = pd.read_csv('patents_data_renewable_energy.csv')
df3 = pd.read_csv('patents_data_wind_power.csv')
df4 = pd.read_csv('patents_data_wind_turbine.csv')
#
df = pd.concat([df1, df2, df3, df4], ignore_index=True)
df.drop_duplicates(inplace=True)
df.to_csv('patents_data_energy.csv', index=False)
