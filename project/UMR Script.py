#!/usr/bin/env python
# coding: utf-8

# In[34]:


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
master_df_UMR = pd.DataFrame(columns=columns)

# Print the DataFrame to verify
print("DataFrame with specified columns:")
print(master_df_UMR)


# In[35]:


import pandas as pd

# Ensure the path is correct and use raw string notation for Windows path
file_path = r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\UMR\76416044 and 76416045 Mthly AGG 2412 1-1-2023 2 (3).csv"
try:
    # Load the CSV file into a DataFrame
    # If your CSV has a header in a specific row, use the 'header' parameter to specify it
    # Use skiprows to start reading data from the correct row
    df = pd.read_csv(file_path)  # Adjust skiprows if needed

    column_labels = [chr(i) for i in range(ord('A'), ord('Z') + 1)]

    # Assign these labels to the DataFrame columns
    df.columns = column_labels[:len(df.columns)]

    # Select specific rows if needed, for example from index 0 to 2 (first three rows)
    df = df.iloc[0:50]
    print(df)  # Adjust range as needed
    # Select specific columns from 'A' to 'O' (0 to 14 index-based)
    table = df.iloc[:, 0:15]  # Adjust this range based on the columns you need

    # Further select rows from 14 to 25 (15th to 26th rows, zero-based index)
    table = table.iloc[15:27]
    new_header = df.iloc[14]
    table.columns = new_header

    value = df.at[4, 'C']

    # Convert to string to slice and extract the values
    value_str = str(value)
    incurred_value = value_str[:2]  # First two characters
    paid_value = value_str[2:]  
    # Print the DataFrame to verify it's loaded and modified correctly
    print("DataFrame:")
    print(table)

    # Extract specific values to a dictionary, similar to cell extraction in Excel
    values_dict = {
        'min_attachment_point': df.at[37, 'F'],  # Example of accessing a value
        'single': df.at[7, 'D'],
        'emp+wife': df.at[8, 'D'],
        'emp_child': df.at[9, 'D'],
        'family': df.at[10, 'D'],
        'incurred': incurred_value,
        'paid' : paid_value
        # Add more key-value pairs as needed
    }

    # Assuming there's a date column to split like before
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


# In[36]:


table.columns


# In[37]:


# Function to remove dollar signs and convert to float
def convert_to_float(value):
    # Check if the value is a string and contains a dollar sign
    if isinstance(value, str) and '$' in value:
        # Remove the dollar sign and commas, then convert to float
        return float(value.replace('$', '').replace(',', ''))
    return value

# Apply the conversion to all elements in the DataFrame
table = table.applymap(convert_to_float)


# In[38]:


table['Medical\nClaims'] = pd.to_numeric(table['Medical\nClaims'].str.replace(',', ''), errors='coerce').fillna(0)
table['Pharmacy\nClaims'] = pd.to_numeric(table['Pharmacy\nClaims'].str.replace(',', ''), errors='coerce').fillna(0)

table['Total Monthly Claims'] = pd.to_numeric(table['Total Monthly Claims'].str.replace(',', ''), errors='coerce').fillna(0)
table['Specific Claims Requested'] = pd.to_numeric(table['Specific Claims Requested'].str.replace(',', ''), errors='coerce').fillna(0)
table['Total Exclusions'] = pd.to_numeric(table['Total Exclusions'].str.replace(',', ''), errors='coerce').fillna(0)


# In[39]:


master_df_UMR['Month']= table['Month']
master_df_UMR['Enrollment - EE']= table['Single EE Count']
master_df_UMR['Enrollment - ES']= table['EE + Spouse or EE + 1']
master_df_UMR['Enrollment - EC']= table['EE + Child(ren)']
master_df_UMR['Enrollment - Fam']= table['Family EE Count']
master_df_UMR['Monthly Attachment']= table['Actual Attachment Point Calc']

#master_df_UMR['Cumlative Attachment']= df['Estimated attachment point year to date']

master_df_UMR['Monthly Medical']= table['Medical\nClaims']

master_df_UMR['Monthly RX']= table['Pharmacy\nClaims']

master_df_UMR['Monthly Total']= table['Total Monthly Claims']

master_df_UMR['Total Medical']= table['Medical\nClaims'].cumsum()

master_df_UMR['Total RX']= table['Pharmacy\nClaims'].cumsum()

master_df_UMR['Total Paid']= table['Total Monthly Claims'].cumsum()

master_df_UMR['Not Covered (Monthly)']= table['Total Exclusions']
master_df_UMR['Not Covered (Running)']= table['Total Exclusions'].cumsum()
master_df_UMR['Spec Claim amount']= table['Specific Claims Requested']
master_df_UMR['Spec Total (running)']= table['Specific Claims Requested'].cumsum()


#master_df_UMR['Total Attchment (Running)']= df['Estimated attachment point year to date']

master_df_UMR['Total Claims (Running)']= table['YTD Eligible Stoploss Claims']
master_df_UMR['Contract Start']= values_dict['contract_start']
master_df_UMR['Contract End']= values_dict['contract_end']
master_df_UMR['Plan Start Date']= values_dict['plan_start_date']
master_df_UMR['Min Attachment Point']= values_dict['min_attachment_point']
#master_df_UMR['Spec Level']= values_dict['spec_level']
master_df_UMR['Agg Factors EE']= values_dict['single']
master_df_UMR['Agg Factors ES']= values_dict['emp+wife']
master_df_UMR['Agg Factors EC']= values_dict['emp_child']
master_df_UMR['Agg Factors Fam']= values_dict['family']
master_df_UMR['Incurred'] = values_dict['incurred']
master_df_UMR['Paid'] = values_dict['paid']


# In[40]:


master_df_UMR['Monthly Total']


# In[41]:


# Function to remove dollar signs and convert to float
def convert_to_float(value):
    # Check if the value is a string and contains a dollar sign
    if isinstance(value, str) and '$' in value:
        # Remove the dollar sign and commas, then convert to float
        return float(value.replace('$', '').replace(',', ''))
    return value

# Apply the conversion to all elements in the DataFrame
master_df_UMR = master_df_UMR.applymap(convert_to_float)


# In[43]:


master_df_UMR.to_csv(r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\master_df\master_df_UMR.csv")


# In[ ]:




