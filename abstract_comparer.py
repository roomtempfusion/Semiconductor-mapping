from fuzzywuzzy import process
import pandas as pd

# Assuming df is your dataframe
df = pd.read_csv('patents_value.csv')


def similarity_ratio(query, choice):
    return process.extractOne(query, [choice])[1]


indices_dropped = []

for i, ivalue in df['patent_abstract'].items():
    print(i)
    if i in indices_dropped:
        continue
    for j, jvalue in df['patent_abstract'].items():
        ratio = similarity_ratio(ivalue, jvalue)
        if ratio > 90 and (i != j):
            df.drop(index=j, inplace=True)
            indices_dropped.append(j)
            # print(f"Will drop index {j} with similarity ratio {ratio}")

# Drop the selected indices

# Reset index after dropping rows

print(df)
df.to_csv('patents_value_cleaned.csv', index=False)