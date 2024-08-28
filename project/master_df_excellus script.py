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
master_df_Excellus = pd.DataFrame(columns=columns)

# Print the DataFrame to verify
print("DataFrame with specified columns:")
print(master_df_Excellus)


import pandas as pd

# Ensure the path is correct and use raw string notation for Windows path
file_path = r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\Excellus\2023 Stop Loss Report & Agg 3.2023.csv"
try:
    # Load the CSV file into a DataFrame
    # If your CSV has a header in a specific row, use the 'header' parameter to specify it
    # Use skiprows to start reading data from the correct row
    df = pd.read_csv(file_path)  # Adjust skiprows if needed

    column_labels = [chr(i) for i in range(ord('A'), ord('Z') + 1)]

    # Assign these labels to the DataFrame columns
    df.columns = column_labels[:len(df.columns)]
    print(df)

    # Select specific rows if needed, for example from index 0 to 2 (first three rows)
    df = df.iloc[0:50]  # Adjust range as needed
    # Select specific columns from 'A' to 'O' (0 to 14 index-based)
    table = df.iloc[:, 0:21]  # Adjust this range based on the columns you need

    # Further select rows from 14 to 25 (15th to 26th rows, zero-based index)
    table = table.iloc[12:35]
    new_header = df.iloc[11]
    table.columns = new_header
    # Print the DataFrame to verify it's loaded and modified correctly
    print("DataFrame:")
    print(table)

    # Extract specific values to a dictionary, similar to cell extraction in Excel
    values_dict = {
        'min_attachment_point': df.at[2, 'K'],
        'spec_level': df.at[4,'K'], # Example of accessing a value
        'single': df.at[9, 'B'],
        'emp+wife': df.at[9, 'C'],
        'emp_child': df.at[9, 'D'],
        'family': df.at[9, 'E'],
        'contract type string' : df.at[4, 'C']

        # Add more key-value pairs as needed
    }

    incurred_paid_string = values_dict['contract type string']

    # Split the string by '/'
    incurred, paid_with_extra = incurred_paid_string.split('/')
    values_dict['incurred'] = incurred
    values_dict['paid'] = paid_with_extra

    # Assuming there's a date column to split like before

    #values_dict['plan_start_date'] = df.at[6, 'C'] 
    date_value = df.at[3, 'C']  # Replace with the actual column name containing the date
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


table['Medical Claims\nPaid']



# Function to remove dollar signs and convert to float
def convert_to_float(value):
    # Check if the value is a string and contains a dollar sign
    if isinstance(value, str) and '$' in value:
        # Remove the dollar sign and commas, then convert to float
        return float(value.replace('$', '').replace(',', ''))
    return value

# Apply the conversion to all elements in the DataFrame
table = table.applymap(convert_to_float)

table

# Ensure the column is numeric, replace non-numeric values with NaN, and fill them with 0
#table['Net Paid'] = pd.to_numeric(table['Net Paid'].str.replace(',', ''), errors='coerce').fillna(0)
#table['Medical Claims\nPaid'] = pd.to_numeric(table['Medical Claims\nPaid'].str.replace(',', ''), errors='coerce').fillna(0)
#table['RX Claims Paid'] = pd.to_numeric(table['RX Claims Paid'].str.replace(',', ''), errors='coerce').fillna(0)

# Calculate the cumulative sum
#table['YTD paid'] = table['Net Paid'].cumsum()
table['Total Medical'] = table['Medical Claims\nPaid'].cumsum()
table['Total RX'] = table['RX Claims Paid'].cumsum()

master_df_Excellus['Month']= table['Month']
master_df_Excellus['Enrollment - EE']= table['Single Contracts']
master_df_Excellus['Enrollment - ES']= table['Emp/Spouse Contracts']
master_df_Excellus['Enrollment - EC']= table['Emp/Child Contracts']
master_df_Excellus['Enrollment - Fam']= table['Family Contracts']
master_df_Excellus['Monthly Attachment']= table['Attachment Point Monthly']

master_df_Excellus['Cumlative Attachment']= table['Attachment Point YTD']

master_df_Excellus['Monthly Medical']= table['Medical Claims\nPaid']

master_df_Excellus['Monthly RX']= table['RX Claims Paid']

master_df_Excellus['Monthly Total']= table['Adjusted Paid Claims Monthly']
master_df_Excellus['Total Medical']= table['Total Medical']

master_df_Excellus['Total RX']= table['Total RX']

master_df_Excellus['Total Paid']= table['Adjusted Paid Claims YTD']

master_df_Excellus['Total Attchment (Running)']= table['Attachment Point YTD']

master_df_Excellus['Total Claims (Running)']= table['Adjusted Paid Claims YTD']

master_df_Excellus['Spec Claim amount'] = table['Claims Exceeding Spec Deductible']
master_df_Excellus['Spec Total (running)'] = table['Claims Exceeding Spec Deductible'].cumsum()


master_df_Excellus['Contract Start']= values_dict['contract_start']
master_df_Excellus['Contract End']= values_dict['contract_end']
master_df_Excellus['Plan Start Date']= values_dict['plan_start_date']
master_df_Excellus['Min Attachment Point']= values_dict['min_attachment_point']
master_df_Excellus['Spec Level']= values_dict['spec_level']
master_df_Excellus['Agg Factors EE']= values_dict['single']
master_df_Excellus['Agg Factors ES']= values_dict['emp+wife']
master_df_Excellus['Agg Factors EC']= values_dict['emp_child']
master_df_Excellus['Agg Factors Fam']= values_dict['family']
master_df_Excellus['Incurred']= values_dict['incurred']
master_df_Excellus['Paid']= values_dict['paid']




# Function to remove dollar signs and convert to float
def convert_to_float(value):
    # Check if the value is a string and contains a dollar sign
    if isinstance(value, str) and '$' in value:
        # Remove the dollar sign and commas, then convert to float
        return float(value.replace('$', '').replace(',', ''))
    return value

# Apply the conversion to all elements in the DataFrame
master_df_Excellus = master_df_Excellus.applymap(convert_to_float)

master_df_Excellus.to_csv(r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\master_df\master_df_excellus.csv")

master_df_Excellus['Month']



