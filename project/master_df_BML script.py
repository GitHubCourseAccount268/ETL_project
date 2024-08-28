#!/usr/bin/env python
# coding: utf-8

# In[275]:


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
master_df_BML = pd.DataFrame(columns=columns)

# Print the DataFrame to verify
print("DataFrame with specified columns:")
print(master_df_BML)


# In[276]:


import pandas as pd

# Ensure the path is correct and use raw string notation for Windows path
file_path = r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\BML\December -22 - Agg report - .csv"
try:
    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path, header=None)  # Load without a header to manually set it later

    # Rename the columns to A, B, C, etc.
    column_labels = [chr(i) for i in range(ord('A'), ord('A') + len(df.columns))]
    df.columns = column_labels

    # Create a new DataFrame with new column labels if needed
    df_label = df.copy()


    # Print the DataFrame to verify it's loaded and modified correctly
    print("Modified DataFrame:")
    print(df)

    # Select specific rows and columns as needed
    table_1 = df.iloc[2:14, 5:12]  # Adjust this range based on the columns you need
    table_2 = df.iloc[20:32, 0:14]
    table_3 = df.iloc[39:51,0:5]

    # Set new headers for table_2

    new_header_1 = df.iloc[0, 5:12].tolist()
    print(new_header_1)
    table_1.columns = new_header_1
    new_header_2 = df.iloc[19].to_list()
    table_2.columns = new_header_2

    # Print the extracted tables
    print("Table 1:")
    print(table_1)
    print("Table 2:")
    print(table_2)

    incurred_paid_string = df_label.at[5,'D']
    incurred, paid = incurred_paid_string.split('/')

    # Extract specific values to a dictionary
    values_dict = {
        'min_attachment_point': df_label.at[9, 'C'],
        'spec_level': df_label.at[7, 'C'],
        'single': df_label.at[1, 'G'],
        'emp+wife': df_label.at[1, 'H'],
        'emp_child': df_label.at[1, 'I'],
        'family': df_label.at[1, 'J'],
        'plan year': df_label.at[0,'C'],
        'incurred':incurred,
        'paid':paid

    }

    date_value = values_dict.get("plan year")
    if date_value and "-" in date_value:
        date_parts = date_value.split('-')
        if len(date_parts) == 2:
            values_dict['contract_start'] = date_parts[0].strip('/')
            values_dict['contract_end'] = date_parts[1].strip('/')
        else:
            print("Unexpected date format in the 'From' value")
    values_dict['plan_start_date'] = values_dict['contract_start']

    # Print the extracted dictionary
    print("Extracted Values Dictionary:")
    print(values_dict)

except Exception as e:
    print(f"An error occurred: {e}")



# In[277]:


table_1


# In[278]:


new_header_3 = df.iloc[38, 0:5].tolist()
table_3.columns = new_header_3
table_3.columns


# In[279]:


table_1


# In[280]:


import pandas as pd
import numpy as np

# Function to remove dollar signs and convert to float
def convert_to_float(value):
    # Check if the value is a string
    if isinstance(value, str):
        # If the value is '$-', treat it as NaN
        if value.strip() == '$-':
            return np.nan
        # If the value contains a dollar sign, remove it and convert to float
        if '$' in value:
            # Remove dollar signs and commas
            cleaned_value = value.replace('$', '').replace(',', '')
            # Check if the cleaned value is a valid number
            try:
                return float(cleaned_value)
            except ValueError:
                return np.nan
    # If the value is already a number, return it as is
    return value


# Apply the conversion to all elements in the DataFrame
table_2 = table_2.applymap(convert_to_float)
table_1 = table_1.applymap(convert_to_float)

table_3 = table_3.applymap(convert_to_float)
# Display


# In[281]:


table_1


# In[282]:


table_3


# In[283]:


#table_2['Medical \nClaims Paid'] = pd.to_numeric(table_2['Medical \nClaims Paid'].str.replace(',', ''), errors='coerce').fillna(0)
#table_2['Pharmacy \nClaims Paid'] = pd.to_numeric(table_2['Pharmacy \nClaims Paid'].str.replace(',', ''), errors='coerce').fillna(0)
#table_1['Monthly Attachment Point'] = pd.to_numeric(table_1['Monthly Attachment Point'].str.replace(',', ''), errors='coerce').fillna(0)
#table_3['Total Outside Contract'] = pd.to_numeric(table_3['Total Outside Contract'].str.replace(',', ''), errors='coerce').fillna(0)


# Calculate the cumulative sum
#table['YTD paid'] = table['Net Paid'].cumsum()
table_2['Total Medical'] = table_2['Pharmacy \nClaims Paid'].cumsum()
table_2['Total RX'] = table_2['Pharmacy \nClaims Paid'].cumsum()
table_1['Cummalative attachment'] = table_1['Monthly Attachment Point'].cumsum()
table_3['Total (running) Outside Contract'] = table_3['Total Outside Contract'].cumsum()



# In[284]:


# Reset index for all tables
table_1.reset_index(drop=True, inplace=True)
table_2.reset_index(drop=True, inplace=True)
table_3.reset_index(drop=True, inplace=True)

# Print the columns of each table to verify
print("Columns in table_1:", table_1.columns)
print("Columns in table_2:", table_2.columns)
print("Columns in table_3:", table_3.columns)


# In[285]:


table_1['Emp/Ch']


# In[286]:


import pandas as pd

# Assuming table_1, table_2, table_3 are already defined and populated DataFrames
# Also assuming master_df_BML is an initialized DataFrame of the appropriate size
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
master_df_BML = pd.DataFrame(columns=columns)

# Print the DataFrame to verify
print("DataFrame with specified columns:")
print(master_df_BML)
# Initialize master_df_BML with the same length as table_2, for example
#master_df_BML = pd.DataFrame(index=table_2.index)

# Assign columns from table_1 and table_2 to master_df_BML
master_df_BML['Month'] = table_2['Month']
master_df_BML['Enrollment - EE'] = table_1['Single']
master_df_BML['Enrollment - ES'] = table_1['Emp/Sp']
master_df_BML['Enrollment - EC'] = table_1['Emp/Ch']
master_df_BML['Enrollment - Fam'] = table_1['Family']
master_df_BML['Monthly Attachment'] = table_1['Monthly Attachment Point']

master_df_BML['Cumlative Attachment'] = table_1['Cummalative attachment']

master_df_BML['Monthly Medical'] = table_2['Medical \nClaims Paid']

master_df_BML['Monthly RX'] = table_2['Pharmacy \nClaims Paid']

master_df_BML['Monthly Total'] = table_2['Total  \nClaims Paid']
master_df_BML['Total Medical'] = table_2['Total Medical']

master_df_BML['Total RX'] = table_2['Total RX']

master_df_BML['Total Paid'] = table_2['Net Claims Paid']

master_df_BML['Total Attchment (Running)'] = table_1['Cummalative attachment']

master_df_BML['Total Claims (Running)'] = table_2['YTD Claims Paid']
master_df_BML['Not Covered (Monthly)'] = table_3['Total Outside Contract']
master_df_BML['Not Covered (Running)'] = table_3['Total (running) Outside Contract']

# Assign values from values_dict
master_df_BML['Contract Start'] = values_dict['contract_start']
master_df_BML['Contract End'] = values_dict['contract_end']
master_df_BML['Plan Start Date'] = values_dict['plan_start_date']
master_df_BML['Min Attachment Point'] = values_dict['min_attachment_point']
master_df_BML['Spec Level'] = values_dict['spec_level']
master_df_BML['Agg Factors EE'] = values_dict['single']
master_df_BML['Agg Factors ES'] = values_dict['emp+wife']
master_df_BML['Agg Factors EC'] = values_dict['emp_child']
master_df_BML['Agg Factors Fam'] = values_dict['family']

master_df_BML['Incurred'] = values_dict['incurred']

master_df_BML['Paid'] = values_dict['paid']

# Print the resulting DataFrame to check the output
print(master_df_BML)


# In[287]:


master_df_BML


# In[288]:


# Function to remove dollar signs and convert to float
def convert_to_float(value):
    # Check if the value is a string and contains a dollar sign
    if isinstance(value, str) and '$' in value:
        # Remove the dollar sign and commas, then convert to float
        return float(value.replace('$', '').replace(',', ''))
    return value

# Apply the conversion to all elements in the DataFrame
master_df_BML = master_df_BML.applymap(convert_to_float)


# In[289]:


master_df_BML['Enrollment - EE']


# In[290]:


master_df_BML.to_csv(r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\master_df\master_df_BML.csv")


# In[ ]:




