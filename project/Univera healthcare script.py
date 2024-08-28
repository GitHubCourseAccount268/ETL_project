#!/usr/bin/env python
# coding: utf-8

# In[33]:


pip install pyexcel pyexcel-xls pyexcel-xlsx


# In[34]:


pip install pandas


# In[35]:


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
master_df = pd.DataFrame(columns=columns)

# Print the DataFrame to verify
print("DataFrame with specified columns:")
print(master_df)


# In[36]:


pip install openpyxl


# In[37]:


import openpyxl

# Ensure the path is correct and use raw string notation for Windows path
file_path = r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\Univera\2022 Stop Loss Report 11.2022 (1).xlsx"

try:
    # Load the workbook and select the "Aggregate" sheet
    workbook = openpyxl.load_workbook(file_path)
    if "Aggregate" in workbook.sheetnames:
        sheet = workbook["Aggregate"]
    else:
        raise ValueError("Sheet named 'Aggregate' not found in the Excel file")

    # Define the cells and their corresponding dictionary keys
    cell_keys = {
        'L5': 'min_attachment_point',
        'L7': 'spec_level',
        'C11': 'single',
        'E11': 'emp+wife',
        'G11': 'emp_child',
        'I11': 'family',
        'C7': 'incurred_paid_string'
    }

    # Extract the cell values and store them in a dictionary
    values_dict = {key: sheet[cell].value for cell, key in cell_keys.items()}

    # Split the incurred and paid values from the 'incurred_paid_string' key
    incurred_paid_value = values_dict['incurred_paid_string']
    if incurred_paid_value:
        incurred, paid = incurred_paid_value.split('/')
        values_dict['incurred'] = int(incurred.strip())
        values_dict['paid'] = int(paid.strip())

    # Handle the date separately to split and assign to contract_start and contract_end
    date_value = sheet['C6'].value
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


# In[38]:


import pandas as pd

# Ensure the path is correct and use raw string notation for Windows path
file_path = r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\Univera\2022 Stop Loss Report 11.2022 (1).xlsx"
try:
    # Load the Excel file and specify the sheet
    # Skip rows before the header (which is on row 11, so you skip the first 10 rows)
    df = pd.read_excel(file_path, sheet_name='Aggregate', header=12, usecols='A:N')

    # Select only the rows from index 2 onwards (which corresponds to starting from row 13 in the original Excel)
    df = df.iloc[0:8]  # This will give you the rows A13 to N22 (zero-based index for pandas)

    # Print the DataFrame to verify it's loaded correctly
    print("DataFrame:")
    print(df)

except Exception as e:
    print(f"An error occurred: {e}")


print(values_dict)


# In[39]:


df


# In[40]:


df.columns


# In[41]:


# Function to remove dollar signs and convert to float
def convert_to_float(value):
    # Check if the value is a string and contains a dollar sign
    if isinstance(value, str) and '$' in value:
        # Remove the dollar sign and commas, then convert to float
        return float(value.replace('$', '').replace(',', ''))
    return value

# Apply the conversion to all elements in the DataFrame
df = df.applymap(convert_to_float)


# In[ ]:





# In[42]:


master_df['Month']= df['Month']
master_df['Enrollment - EE']= df['Single']
master_df['Enrollment - ES']= df['Emp + Spouse']
master_df['Enrollment - EC']= df['Emp + Child']
master_df['Enrollment - Fam']= df['Family']
master_df['Monthly Attachment']= df['Estimated attachment point monthly']

master_df['Cumlative Attachment']= df['Estimated attachment point year to date']

master_df['Monthly Medical']= df['Medical paid this month']

master_df['Monthly RX']= df['RX Claims paid this month']

master_df['Monthly Total']= df['\nClaims paid year to date']

master_df['Total Medical']= df['Medical paid this month'].cumsum()

master_df['Total RX']= df['RX Claims paid this month'].cumsum()

master_df['Total Paid']= df['\nClaims paid year to date'].cumsum()

master_df['Total Attchment (Running)']= df['Estimated attachment point year to date']

master_df['Total Claims (Running)']= df['\nClaims paid year to date']
master_df['Spec Claim amount']= df['Specific excess reimbursement']
master_df['Spec Total (running)']= df['Specific excess reimbursement'].cumsum()
master_df['Contract Start']= values_dict['contract_start']
master_df['Contract End']= values_dict['contract_end']
master_df['Plan Start Date']= values_dict['plan_start_date']
master_df['Min Attachment Point']= values_dict['min_attachment_point']
master_df['Spec Level']= values_dict['spec_level']
master_df['Agg Factors EE']= values_dict['single']
master_df['Agg Factors ES']= values_dict['emp+wife']
master_df['Agg Factors EC']= values_dict['emp_child']
master_df['Agg Factors Fam']= values_dict['family']
master_df['Incurred'] = values_dict['incurred']
master_df['Paid'] = values_dict['paid']


# In[43]:


master_df['Total Paid']


# In[12]:


Extracted Values Dictionary:
{'min_attachment_point': 1518622, 'spec_level': 125000, 'single': 726.93, 'emp+wife': 1448.04, 'emp_child': 1281.57, 'family': 2174.96, 'contract_start': '5/1/22', 'plan_start_date': '5/1/22', 'contract_end': '12/31/22'}


# In[45]:


master_df


# In[44]:


# Function to remove dollar signs and convert to float
def convert_to_float(value):
    # Check if the value is a string and contains a dollar sign
    if isinstance(value, str) and '$' in value:
        # Remove the dollar sign and commas, then convert to float
        return float(value.replace('$', '').replace(',', ''))
    return value

# Apply the conversion to all elements in the DataFrame
master_df = master_df.applymap(convert_to_float)


# In[46]:


master_df.to_csv(r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\master_df\master_df_univera.csv")



# In[ ]:




