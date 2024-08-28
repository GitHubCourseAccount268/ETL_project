#!/usr/bin/env python
# coding: utf-8

# In[2]:


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
master_df_coeur_old = pd.DataFrame(columns=columns)

# Print the DataFrame to verify
print("DataFrame with specified columns:")
print(master_df_coeur_old)


# In[3]:


import pandas as pd

# Ensure the path is correct and use raw string notation for Windows path
file_path = r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\Coeur_old\OLD - _SL Reinsurance Rpt_2023_12.csv"
try:
    # Load the CSV file into a DataFrame
    # If your CSV has a header in a specific row, use the 'header' parameter to specify it
    # Use skiprows to start reading data from the correct row
    df = pd.read_csv(file_path)  # Adjust skiprows if needed

    column_labels = [chr(i) for i in range(ord('A'), ord('Z') + 1)]

    # Assign these labels to the DataFrame columns
    df.columns = column_labels[:len(df.columns)]

    # Select specific rows if needed, for example from index 0 to 2 (first three rows)
    #df = df.iloc[0:50]  # Adjust range as needed
    # Select specific columns from 'A' to 'O' (0 to 14 index-based)
    table = df.iloc[0:50, 0:22]  # Adjust this range based on the columns you need

    # Further select rows from 14 to 25 (15th to 26th rows, zero-based index)
    table = table.iloc[9:21]
    new_header = df.iloc[8]
    table.columns = new_header
    # Print the DataFrame to verify it's loaded and modified correctly
    print("DataFrame:")
    print(table)

    # Extract specific values to a dictionary, similar to cell extraction in Excel
    values_dict = {
        'min_attachment_point': df.at[1, 'R'],
        'spec_level': df.at[2,'R'], # Example of accessing a value
        'single': df.at[5, 'C'],
        'emp+wife': df.at[5, 'D'],
        'emp_child': df.at[5, 'E'],
        'family': df.at[5, 'F'],
        # Add more key-value pairs as needed
    }

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


# In[4]:


new_column_names = {
    'Claims': ['Monthly_medical_claims', 'Monthly_total']
}

# Update column names to avoid repetition
current_column_names = table.columns.tolist()
updated_column_names = []
counter = {name: 0 for name in new_column_names}

for name in current_column_names:
    if name in new_column_names:
        updated_name = new_column_names[name][counter[name]]
        updated_column_names.append(updated_name)
        counter[name] += 1
    else:
        updated_column_names.append(name)

# Rename the columns in the DataFrame
table.columns = updated_column_names


# In[5]:


table.columns


# In[6]:


table['Monthly_medical_claims'] = pd.to_numeric(table['Monthly_medical_claims'].str.replace(',', ''), errors='coerce').fillna(0)
table['Rx Claims'] = pd.to_numeric(table['Rx Claims'].str.replace(',', ''), errors='coerce').fillna(0)

# Calculate the cumulative sum
#table['YTD paid'] = table['Net Paid'].cumsum()
table['Total Medical'] = table['Monthly_medical_claims'].cumsum()
table['Total RX'] = table['Rx Claims'].cumsum()


# In[7]:


master_df_coeur_old['Month']= table['(MM/YYYY)']
master_df_coeur_old['Enrollment - EE']= table['EE']
master_df_coeur_old['Enrollment - ES']= table['ES']
master_df_coeur_old['Enrollment - EC']= table['EC']
master_df_coeur_old['Enrollment - Fam']= table['FM']
master_df_coeur_old['Monthly Attachment']= table['Deposit']

master_df_coeur_old['Cumlative Attachment']= table['Year-to-Date']

master_df_coeur_old['Monthly Medical']= table['Monthly_medical_claims']

master_df_coeur_old['Monthly RX']= table['Rx Claims']

master_df_coeur_old['Monthly Total']= table['Monthly_total']
master_df_coeur_old['Total Medical']= table['Total Medical']

master_df_coeur_old['Total RX']= table['Total RX']

master_df_coeur_old['Total Paid']= table['Claims YTD']

master_df_coeur_old['Total Attchment (Running)']= table['Year-to-Date']

master_df_coeur_old['Total Claims (Running)']= table['Claims YTD']
master_df_coeur_old['Contract Start']= values_dict['contract_start']
master_df_coeur_old['Contract End']= values_dict['contract_end']
master_df_coeur_old['Contract Start']= values_dict['plan_start_date']
master_df_coeur_old['Min Attachment Point']= values_dict['min_attachment_point']
master_df_coeur_old['Spec Level']= values_dict['spec_level']
master_df_coeur_old['Agg Factors EE']= values_dict['single']
master_df_coeur_old['Agg Factors ES']= values_dict['emp+wife']
master_df_coeur_old['Agg Factors EC']= values_dict['emp_child']
master_df_coeur_old['Agg Factors Fam']= values_dict['family']


# In[8]:


master_df_coeur_old.to_csv(r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\master_df\master_df_Coeur_Old.csv")


# In[ ]:




