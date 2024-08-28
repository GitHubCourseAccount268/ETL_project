import pandas as pd

# Define the column names
columns = [
    "Group Id", "Group Name", "Contract Year ID", "Contract Type", "Contract Year",
    "Contract Start", "Contract End", "Incurred", "Paid", "Plan Start Date",
    "Min Attachment Point", "Spec Level", "Monthly Attachment", "Cumlative Attachment",
    "Month", "Monthly Medical", "Monthly RX", "Monthly Total", "Not Covered (Monthly)",
    "Not Covered (Running)", "Total Medical", "Total RX", "Total Paid",
    "Total Attchment (Running)", "Total Claims (Running)", "Spec Claim amount",
    "Spec Total (running)", "Laser Amount", "Enrollment - EE", "Enrollment - ES",
    "Enrollment - EC", "Enrollment - Fam", "Spec claimant ID", "Spec Claimant Gender",
    "Spec Claimant Amount", "Spec Claimant age", "Agg Factors EE", "Agg Factors ES",
    "Agg Factors EC", "Agg Factors Fam", "Enrollment member- EE", "Enrollment member - ES",
    "Enrollment member - EC", "Enrollment member- Fam", "Reduction", "Reduction running",
    "Plan ID", "ASD", "Other Claims", "Other Claim total"
]

# Create an empty DataFrame with the specified column names
master_df_Aither = pd.DataFrame(columns=columns)

# Print the DataFrame to verify
print("DataFrame with specified columns:")
print(master_df_Aither)


import pandas as pd

# Ensure the path is correct and use raw string notation for Windows path
file_path = r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\Aither\Aggregate Report_RUNOUT (1).csv"

import string

def generate_column_labels(num_columns):
    alphabet = string.ascii_uppercase  # 'A' to 'Z'
    labels = []
    
    # Single letters
    labels.extend(alphabet)
    
    # Double letters (AA, AB, ..., ZZ)
    for first in alphabet:
        for second in alphabet:
            labels.append(first + second)
            if len(labels) == num_columns:
                return labels

    return labels


try:
    # Load the CSV file into a DataFrame
    # If your CSV has a header in a specific row, use the 'header' parameter to specify it
    # Use skiprows to start reading data from the correct row
    df = pd.read_csv(file_path)
    # print(df)  # Adjust skiprows if needed

    column_labels = generate_column_labels(257)
    
    # Assign these labels to the DataFrame columns
    df.columns = column_labels[:len(df.columns)]

    # Select specific rows if needed, for example from index 0 to 2 (first three rows)
    df = df.iloc[0:50]  # Adjust range as needed
    print(df)
    # Select specific columns from 'A' to 'O' (0 to 14 index-based)
    table = df.iloc[:, 0:257]  # Adjust this range based on the columns you need
    # Further select rows from 14 to 25 (15th to 26th rows, zero-based index)
    table = table.iloc[11:26]
    new_header = df.iloc[10]
    #print(new_header)
    table.columns = new_header
    #print(table.columns)
    # Print the DataFrame to verify it's loaded and modified correctly
    print("DataFrame:")
    print(table)

    # Extract specific values to a dictionary, similar to cell extraction in Excel
    values_dict = {
        'min_attachment_point': df.at[8, 'F'],
        'spec_level': df.at[5,'F'], # Example of accessing a value
        'single': df.at[5, 'J'],
        'emp+wife': df.at[6, 'J'],
        'emp_child': df.at[7, 'J'],
        'family': df.at[8, 'J'],
        'incurred':df.at[1,'J'],
        'paid':df.at[2,'J']
        # Add more key-value pairs as needed
    }

    # Assuming there's a date column to split like before

    #values_dict['plan_start_date'] = df.at[6, 'C'] 
    date_value = df.at[1, 'J']  # Replace with the actual column name containing the date
    if pd.notna(date_value):
        date_parts = str(date_value).split('-')
        if len(date_parts) == 2:
            values_dict['contract_start'] = date_parts[0].strip()
            values_dict['plan_start_date'] = date_parts[0].strip()
            values_dict['contract_end'] = date_parts[1].strip()
        else:
            print("Unexpected date format in the specified column")

    # Print the extracted dictionary
    print("Extracted Values Dictionary:")
    print(values_dict)

except Exception as e:
    print(f"An error occurred: {e}")


table.columns# Select the first 20 rows and first 15 columns of the DataFrame
subset_table = table.iloc[:, :15]

# Show the columns of the subset
subset_table_columns = subset_table.columns
subset_table_columns




# Function to remove dollar signs and convert to float
def convert_to_float(value):
    # Check if the value is a string and contains a dollar sign
    if isinstance(value, str) and '$' in value:
        # Remove the dollar sign and commas, then convert to float
        return float(value.replace('$', '').replace(',', ''))
    return value

# Apply the conversion to all elements in the DataFrame
table = table.applymap(convert_to_float)

#table['Medical Claims\nPaid'] = pd.to_numeric(table['Medical Claims\nPaid'].str.replace(',', ''), errors='coerce').fillna(0)
#table['Rx Claims \nPaid'] = pd.to_numeric(table['Rx Claims \nPaid'].str.replace(',', ''), errors='coerce').fillna(0)
#table_1['Monthly \nPaid Claims'] = pd.to_numeric(table_1['Monthly \nPaid Claims'].str.replace(',', ''), errors='coerce').fillna(0)
print(table['Medical Claims\nPaid'])
# Calculate the cumulative sum
#table['YTD paid'] = table['Net Paid'].cumsum()
table['Total Medical'] = table['Medical Claims\nPaid'].cumsum()
table['Total RX'] = table['Rx Claims \nPaid'].cumsum()


table['Total <Less>Amount over SL deductible'] = table['<Less>Amount over SL deductible'].cumsum()
print(table['<Less>Amount over SL deductible'])

#table_1['Cummalative attachment'] = table_1['Monthly \nPaid Claims'].cumsum()

master_df_Aither['Month']= table['Month']
master_df_Aither['Enrollment - EE']= table['# of Employees\nSingle']
master_df_Aither['Enrollment - ES']= table['# of Employees + Spouse']
master_df_Aither['Enrollment - EC']= table['# of Employees + Children']
master_df_Aither['Enrollment - Fam']= table['# of Employees\nFamily']
master_df_Aither['Monthly Attachment']= table['Est. Att.\nMonthly']

master_df_Aither['Cumlative Attachment']= table['Est. Att YTD ']

master_df_Aither['Monthly Medical']= table['Medical Claims\nPaid']

master_df_Aither['Monthly RX']= table['Rx Claims \nPaid']

master_df_Aither['Monthly Total']= table['Monthly\nPaid Claims']
master_df_Aither['Total Medical']= table['Total Medical']

master_df_Aither['Total RX']= table['Total RX']

master_df_Aither['Total Paid']= table['Claims Pd. \nY-T-D']

master_df_Aither['Total Attchment (Running)']= table['Est. Att YTD ']

master_df_Aither['Total Claims (Running)']= table['Claims Pd. \nY-T-D']

master_df_Aither['Spec Claim amount']= table['<Less>Amount over SL deductible']
master_df_Aither['Spec Total (running)']= table['Total <Less>Amount over SL deductible']

master_df_Aither['Contract Start']= values_dict['contract_start']
master_df_Aither['Contract End']= values_dict['contract_end']
master_df_Aither['Plan Start Date']= values_dict['plan_start_date']
master_df_Aither['Min Attachment Point']= values_dict['min_attachment_point']
master_df_Aither['Spec Level']= values_dict['spec_level']
master_df_Aither['Agg Factors EE']= values_dict['single']
master_df_Aither['Agg Factors ES']= values_dict['emp+wife']
master_df_Aither['Agg Factors EC']= values_dict['emp_child']
master_df_Aither['Agg Factors Fam']= values_dict['family']
master_df_Aither['Paid']= values_dict['paid']
master_df_Aither['Incurred']= values_dict['incurred']



master_df_Aither['Contract Start']



# Function to remove dollar signs and convert to float
def convert_to_float(value):
    # Check if the value is a string and contains a dollar sign
    if isinstance(value, str) and '$' in value:
        # Remove the dollar sign and commas, then convert to float
        return float(value.replace('$', '').replace(',', ''))
    return value

# Apply the conversion to all elements in the DataFrame
master_df_Aither = master_df_Aither.applymap(convert_to_float)

master_df_Aither.to_csv(r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\master_df\master_df_Aither.csv")



