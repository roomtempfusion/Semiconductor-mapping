# Combines author and IEEE keywords into one column

import pandas as pd
import json
import matplotlib.pyplot as plt

# df['Author Keywords'] = df['Author Keywords'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
# df['IEEE Terms'] = df['IEEE Terms'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
# df['Keywords'] = df['Author Keywords'] + df['IEEE Terms']
# df.drop(columns=['Author Keywords', 'IEEE Terms'], inplace=True)
# df['Keywords'] = df['Keywords'].apply(lambda x: json.dumps(x) if isinstance(x, (list, set)) else x)
#
# df.to_csv('exploded_uk_affiliations_combinedkeys.csv', index=False)