import pandas as pd
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', None)

excel_file = 'dataentry_EURAF_Draft 1.xlsx'

# Load Excel file into a pandas ExcelFile object
xls = pd.ExcelFile(excel_file)

# Iterate over each sheet in the Excel file
i = 0
for sheet_name in xls.sheet_names:
    i += 1
    if i == 6:
        break
    # Read the sheet into a pandas DataFrame
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    subset_df = df.iloc[2:, 1:]
    if i == 1:
        subset_df.columns = ['InstID', 'Region', 'Institution', 'Type', 'Country', 'State', 'City',
                             'Design', 'Manufacturing', 'Application', 'Basic Research']
        columns_to_check = ['Institution']
    elif i ==2:
        subset_df.columns = ['SubInstID', 'SubInstName', 'InstName', 'State/Province', 'City', 'Primary Contact Name',
                             'Primary Contact Email', 'Primary Contact Website']
        columns_to_check = ['SubInstName']
    elif i == 3:
        subset_df.columns = ['RFNum', 'RFName', 'R&D Capability', 'InstName', 'SubInstName']
        columns_to_check = ['RFName']
    elif i == 4:
        subset_df = df.iloc[2:, 1:6]
        subset_df.columns = ['Institution', 'DonatingInst', 'Collaboration Type', 'Funding Amount', 'Currency']
        columns_to_check = ['Institution', 'DonatingInst']
    elif i == 5:
        subset_df.columns = ['InstName', 'Research Area']
        columns_to_check = ['InstName', 'Research Area']
    nan_rows = subset_df[columns_to_check].isna().any(axis=1)

    # Check if NaN values are found and perform operations accordingly
    if nan_rows.any():
        first_nan_index = nan_rows[nan_rows].index[0]
        # Slice the DataFrame to keep only rows before the first NaN index
        subset_df = subset_df.iloc[:first_nan_index]
    if len(subset_df) > 3:
        val = subset_df.iloc[-2, 1]
        print(val)
        if pd.isna(val):
            subset_df = subset_df.iloc[:-2, :]
    print(subset_df)
    csv_file = f'EURAFR_{i}.csv'

    # Save the DataFrame to a CSV file
    subset_df.to_csv(csv_file, index=False)

