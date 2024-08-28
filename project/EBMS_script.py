#!/usr/bin/env python
# coding: utf-8

# In[22]:


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
master_df_EBMS = pd.DataFrame(columns=columns)

# Print the DataFrame to verify
print("DataFrame with specified columns:")
print(master_df_EBMS)


# In[23]:


import openpyxl

# Ensure the path is correct and use raw string notation for Windows path
file_path = r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\EBMS\042024 Aggregate Summary AGG24.xlsx"
try:
    # Load the workbook and select the "aggregate" sheet
    workbook = openpyxl.load_workbook(file_path)
    if "Sheet1" in workbook.sheetnames:
        sheet = workbook["Sheet1"]
    else:
        raise ValueError("Sheet named 'Sheet1' not found in the Excel file or maybe sheet name is wrong")

    # Define the cells and their corresponding dictionary keys
    cell_keys = {
        'L4': 'min_attachment_point',
        'L7': 'spec_level',
        'E11': 'single',
        'F11': 'emp+wife',
        'G11': 'emp_child',
        'H11': 'family',
        'L2':'contract type string'
    }

    # Extract the cell values and store them in a dictionary
    values_dict = {key: sheet[cell].value for cell, key in cell_keys.items()}


    incurred_paid_string = values_dict['contract type string']

    # Split the string by '/'
    incurred, paid_with_extra = incurred_paid_string.split('/')
    values_dict['incurred'] = incurred
    values_dict['paid'] = paid_with_extra
    # Handle the date separately to split and assign to contract_start and contract_end
    date_value = sheet['E3'].value
    if date_value:
        # Assuming date_value is in format 'start-end'
        date_parts = str(date_value).split('-')
        if len(date_parts) == 2:
            values_dict['contract_start'] = date_parts[0].strip()
            values_dict['plan_start_date'] = date_parts[0].strip()
            values_dict['contract_end'] = date_parts[1].strip()
        else:
            print("Unexpected date format in C6")

    # Print the resulting dictionary
    print("Extracted Values Dictionary:")
    print(values_dict)

except Exception as e:
    print(f"An error occurred: {e}")


# In[24]:


import pandas as pd

# Ensure the path is correct and use raw string notation for Windows path
col_names = ['Month_date', 'EMP',	'ESP'	,'ECH'	,'FAM']

file_path = r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\EBMS\042024 Aggregate Summary AGG24.xlsx"
try:
    # Load the Excel file and specify the sheet
    # Skip rows before the header (which is on row 11, so you skip the first 10 rows)
    enrollment_df = pd.read_excel(file_path, sheet_name='Sheet1', header=10, usecols='D:H')

    amount_df = pd.read_excel(file_path, sheet_name='Sheet1', header=16, usecols='B:Q')

    enrollment_df.columns = col_names
    # Select only the rows from index 2 onwards (which corresponds to starting from row 13 in the original Excel)
    enrollment_df = enrollment_df.iloc[0:4]  # This will give you the rows A13 to N22 (zero-based index for pandas)
    amount_df = amount_df.iloc[0:4]
    # Print the DataFrame to verify it's loaded correctly
    print("DataFrame:")
    print(enrollment_df)
    print(amount_df)
except Exception as e:
    print(f"An error occurred: {e}")

print(values_dict)


# In[ ]:





# In[29]:


master_df_EBMS['Month']= amount_df['Month']
master_df_EBMS['Enrollment - EE']= enrollment_df['EMP']
master_df_EBMS['Enrollment - ES']= enrollment_df['ESP']
master_df_EBMS['Enrollment - EC']= enrollment_df['ECH']
master_df_EBMS['Enrollment - Fam']= enrollment_df['FAM']
master_df_EBMS['Monthly Attachment']= amount_df['Monthly Attachmnt Point']

master_df_EBMS['Cumlative Attachment']= amount_df['Accum Attachmnt Point']

master_df_EBMS['Monthly Medical']= amount_df['Medical']

master_df_EBMS['Monthly RX']= amount_df['RX']

master_df_EBMS['Monthly Total']= amount_df['Net Claims Paid']
master_df_EBMS['Total Medical']= amount_df['Medical'].cumsum()

master_df_EBMS['Total RX']= amount_df['RX'].cumsum()

master_df_EBMS['Total Paid']= amount_df['Net Claims Paid'].cumsum()

master_df_EBMS['Total Attchment (Running)']= amount_df['Accum Attachmnt Point']

master_df_EBMS['Total Claims (Running)']= amount_df['Accum Net Claims Paid']

master_df_EBMS['Not Covered (Monthly)'] = amount_df['Not Covered']
master_df_EBMS['Not Covered (Running)'] = amount_df['Not Covered'].cumsum()
master_df_EBMS['Spec Claim amount'] = amount_df['Over Specific']
master_df_EBMS['Spec Total (running)'] = amount_df['Over Specific'].cumsum()


master_df_EBMS['Contract Start']= values_dict['contract_start']
master_df_EBMS['Contract End']= values_dict['contract_end']
master_df_EBMS['Plan Start Date']= values_dict['plan_start_date']
master_df_EBMS['Min Attachment Point']= values_dict['min_attachment_point']
master_df_EBMS['Spec Level']= values_dict['spec_level']
master_df_EBMS['Agg Factors EE']= values_dict['single']
master_df_EBMS['Agg Factors ES']= values_dict['emp+wife']
master_df_EBMS['Agg Factors EC']= values_dict['emp_child']
master_df_EBMS['Agg Factors Fam']= values_dict['family']
master_df_EBMS['Incurred'] = values_dict['incurred']
master_df_EBMS['Paid'] = values_dict['paid']


# In[30]:


master_df_EBMS


# In[31]:


# Function to remove dollar signs and convert to float
def convert_to_float(value):
    # Check if the value is a string and contains a dollar sign
    if isinstance(value, str) and '$' in value:
        # Remove the dollar sign and commas, then convert to float
        return float(value.replace('$', '').replace(',', ''))
    return value

# Apply the conversion to all elements in the DataFrame
master_df_EBMS = master_df_EBMS.applymap(convert_to_float)


# In[32]:


master_df_EBMS.to_csv(r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\master_df\master_df_EBMS.csv")



# In[ ]:


amount_df['Medical'] = pd.to_numeric(amount_df['Medical'].str.replace(',', ''), errors='coerce').fillna(0)
amount_df['RX'] = pd.to_numeric(amount_df['RX'].str.replace(',', ''), errors='coerce').fillna(0)
amount_df['Net Claims Paid'] = pd.to_numeric(amount_df['Net Claims Paid'].str.replace(',', ''), errors='coerce').fillna(0)
amount_df['Not Covered'] = pd.to_numeric(amount_df['Not Covered'].str.replace(',', ''), errors='coerce').fillna(0)
amount_df['Over Specific'] = pd.to_numeric(amount_df['Over Specific'].str.replace(',', ''), errors='coerce').fillna(0)

