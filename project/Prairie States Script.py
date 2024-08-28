#!/usr/bin/env python
# coding: utf-8

# In[49]:


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
master_df_Prairie_States = pd.DataFrame(columns=columns)

# Print the DataFrame to verify
print("DataFrame with specified columns:")
print(master_df_Prairie_States)


# In[50]:


import pandas as pd

# Ensure the path is correct and use raw string notation for Windows path
file_path = r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\Prairie States\Aggregate Report.csv"
try:
    # Load the CSV file into a DataFrame
    # If your CSV has a header in a specific row, use the 'header' parameter to specify it
    # Use skiprows to start reading data from the correct row
    df = pd.read_csv(file_path)  # Adjust skiprows if needed

    column_labels = [chr(i) for i in range(ord('A'), ord('Z') + 1)]

    # Assign these labels to the DataFrame columns
    df.columns = column_labels[:len(df.columns)]

    # Select specific rows if needed, for example from index 0 to 2 (first three rows)
    df = df.iloc[0:50]  # Adjust range as needed
    
    # Select specific columns from 'A' to 'O' (0 to 14 index-based)
    print(df)
    
    table = df.iloc[:, 0:21]  # Adjust this range based on the columns you need

    # Further select rows from 14 to 25 (15th to 26th rows, zero-based index)
    table = table.iloc[15:27]
    new_header = df.iloc[13]
    table.columns = new_header
    # Print the DataFrame to verify it's loaded and modified correctly
    print("DataFrame:")
    print(table)

    # Extract specific values to a dictionary, similar to cell extraction in Excel
    values_dict = {
        'min_attachment_point': df.at[7, 'O'],
        'spec_level': df.at[4,'O'], # Example of accessing a value
        'single': df.at[33, 'F'],
        'emp+wife': df.at[32, 'F'],
        'emp_child': df.at[31, 'F'],
        'family': df.at[34, 'F'],
        'paid': df.at[8,'C'],
        'incurred': df.at[9,'C']
        # Add more key-value pairs as needed
    }

    # Assuming there's a date column to split like before

    values_dict['plan_start_date'] = df.at[6, 'C'] 
    values_dict['contract_start'] = df.at[6, 'C'] 
    """date_value = df.at[6, 'C']  # Replace with the actual column name containing the date
    if pd.notna(date_value):
        date_parts = str(date_value).split('-')
        if len(date_parts) == 2:
            values_dict['contract_start'] = date_parts[0].strip()
            values_dict['plan_start_date'] = date_parts[0].strip()
            #values_dict['contract_end'] = date_parts[1].strip()
        else:
            print("Unexpected date format in the specified column")"""

    # Print the extracted dictionary
    print("Extracted Values Dictionary:")
    print(values_dict)

except Exception as e:
    print(f"An error occurred: {e}")


# In[51]:


table


# In[52]:


table.columns


# In[53]:


new_col_names = [                           'nan',                   'Month Paid',
                            'EE Only',                            'nan',
                                  'nan',                            'nan',
                         'EE + Child',                            'nan',
                        'EE + Spouse',                       'Family',
                                  'nan',                        'Month',
                                'YTD',                      'Medical',
                                  'nan',                            'nan',
       'Prescription (from PBM Feed)',                            'nan',
                      'Spec Reimbursement',                     'Net Paid',
                      'Reimbursement',                    ]
table.columns = new_col_names


# In[54]:


# Ensure the column is numeric, replace non-numeric values with NaN, and fill them with 0
table['Net Paid'] = pd.to_numeric(table['Net Paid'].str.replace(',', ''), errors='coerce').fillna(0)
table['Medical'] = pd.to_numeric(table['Medical'].str.replace(',', ''), errors='coerce').fillna(0)
table['Prescription (from PBM Feed)'] = pd.to_numeric(table['Prescription (from PBM Feed)'].str.replace(',', ''), errors='coerce').fillna(0)
table['Spec Reimbursement'] = pd.to_numeric(table['Spec Reimbursement'].str.replace(',', ''), errors='coerce').fillna(0)

# Calculate the cumulative sum
table['YTD paid'] = table['Net Paid'].cumsum()
table['Total Medical'] = table['Medical'].cumsum()
table['Total RX'] = table['Prescription (from PBM Feed)'].cumsum()


# In[55]:


table.columns


# In[56]:


master_df_Prairie_States['Month']= table['Month Paid']
master_df_Prairie_States['Enrollment - EE']= table['EE Only']
master_df_Prairie_States['Enrollment - ES']= table['EE + Spouse']
master_df_Prairie_States['Enrollment - EC']= table['EE + Child']
master_df_Prairie_States['Enrollment - Fam']= table['Family']
master_df_Prairie_States['Monthly Attachment']= table['Month']

master_df_Prairie_States['Cumlative Attachment']= table['YTD']

master_df_Prairie_States['Monthly Medical']= table['Medical']

master_df_Prairie_States['Monthly RX']= table['Prescription (from PBM Feed)']

master_df_Prairie_States['Monthly Total']= table['Net Paid']
master_df_Prairie_States['Total Medical']= table['Total Medical']

master_df_Prairie_States['Total RX']= table['Total RX']

master_df_Prairie_States['Total Paid']= table['YTD paid']

master_df_Prairie_States['Total Attchment (Running)']= table['YTD']

master_df_Prairie_States['Total Claims (Running)']= table['YTD paid']
master_df_Prairie_States['Spec Claim amount'] = table['Spec Reimbursement']
master_df_Prairie_States['Spec Total (running)'] = table['Spec Reimbursement'].cumsum()

master_df_Prairie_States['Contract Start']= values_dict['contract_start']
#master_df_Prairie_States['Contract End']= values_dict['contract_end']
master_df_Prairie_States['Plan Start Date']= values_dict['plan_start_date']
master_df_Prairie_States['Min Attachment Point']= values_dict['min_attachment_point']
master_df_Prairie_States['Spec Level']= values_dict['spec_level']
master_df_Prairie_States['Agg Factors EE']= values_dict['single']
master_df_Prairie_States['Agg Factors ES']= values_dict['emp+wife']
master_df_Prairie_States['Agg Factors EC']= values_dict['emp_child']
master_df_Prairie_States['Agg Factors Fam']= values_dict['family']

master_df_Prairie_States['Incurred'] = values_dict['incurred']
master_df_Prairie_States['Paid'] = values_dict['paid']


# In[57]:


master_df_Prairie_States['Contract End']


# In[58]:


master_df_Prairie_States['Contract Start'] = pd.to_datetime(master_df_Prairie_States['Contract Start'], errors='coerce')
master_df_Prairie_States['Contract End'] = pd.to_datetime(master_df_Prairie_States['Contract End'], errors='coerce')
master_df_Prairie_States['Plan Start Date'] = pd.to_datetime(master_df_Prairie_States['Plan Start Date'], errors='coerce')


# In[60]:


master_df_Prairie_States['Contract Start']


# In[61]:


# Function to remove dollar signs and convert to float
def convert_to_float(value):
    # Check if the value is a string and contains a dollar sign
    if isinstance(value, str) and '$' in value:
        # Remove the dollar sign and commas, then convert to float
        return float(value.replace('$', '').replace(',', ''))
    return value

# Apply the conversion to all elements in the DataFrame
master_df_Prairie_States = master_df_Prairie_States.applymap(convert_to_float)


# In[62]:


master_df_Prairie_States.to_csv(r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\master_df\master_df_Prairie.csv")


# In[ ]:




