#!/usr/bin/env python
# coding: utf-8

# In[165]:


import tabula
import fitz  # PyMuPDF
import pandas as pd
import re

def extract_tables_from_pdf(pdf_path):
    # Use tabula to read tables from the entire PDF
    tables = tabula.read_pdf(pdf_path, pages="all", multiple_tables=True)
    return tables

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

def extract_specific_values(text, labels):
    extracted_data = {}
    for label in labels:
        # Use a regular expression to find the label and capture the following text
        pattern = re.compile(rf"{label}\s*([^\n]*)", re.IGNORECASE)
        match = pattern.search(text)
        if match:
            extracted_data[label] = match.group(1).strip()
    return extracted_data

def parse_agg_factors(agg_factors):
    parsed_factors = {}
    # Regular expression to capture different parts of the Agg Factors line
    pattern = re.compile(r"(EMPLOYEE|EE\+SPOUSE|FAMILY|EE\+CHILDREN):\s*\$(\d+\.\d{2})")
    matches = pattern.findall(agg_factors)
    for key, value in matches:
        parsed_factors[key] = float(value)  # Convert the extracted value to a float
    return parsed_factors

def parse_effective_date(effective_str):
    # Regular expression to extract the date from the 'Effective' string
    pattern = re.compile(r"Date of Plan:\s*(\d{1,2}/\d{1,2}/\d{4})")
    match = pattern.search(effective_str)
    if match:
        return match.group(1)  # Return the extracted date
    return "Not Found"

def parse_contract_values(contract_str):
    print(contract_str)
    # Regular expression to extract the incurred and paid values from the 'Contract' string
    pattern = re.compile(r"(\d+)/(\d+)")
    match = pattern.search(contract_str)
    
    if match:
        incurred, paid = match.groups()
        return int(incurred), int(paid)  # Return as integers
    
    return None, None

pdf_path = r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\pdf\JP Farley\Aggregate Report copy 2.pdf"
labels = ["Specific Deductible Specific Max:", "Incurred From:", "To:","Contract Type", "Group:","ContractTpye:"]

# Extracting tables
tables = extract_tables_from_pdf(pdf_path)
#df = pd.DataFrame()
# Storing tables as separate DataFrames
dataframes = {}
for i, table in enumerate(tables):
    df_name = f'table_{i + 1}'
    #df_temp = table
    #df = pd.concat([df, df_temp],ignore_index =True)
    dataframes[df_name] = pd.DataFrame(table)
#df

# Extracting text from the PDF
text = extract_text_from_pdf(pdf_path)

text_lines = text.splitlines()
for index, line in enumerate(text_lines):
    print(f"Index {index}: {line}")

# Extracting specific values
specific_values = extract_specific_values(text, labels)

# Parse the 'Agg Factors' and 'Effective' fields
agg_factors = specific_values.get("Agg Factors", "")
parsed_factors = parse_agg_factors(agg_factors)
specific_values.update(parsed_factors)

# Extract and parse dates and contract values
effective_date_str = specific_values.get("Plan Year:", "")
plan_start_date = parse_effective_date(effective_date_str)

contract_str = specific_values.get("ContractType:", "")
print(contract_str)
incurred, paid = parse_contract_values(contract_str)

contract_str = text_lines[5]
incurred, paid = parse_contract_values(contract_str)

# Store specific extracted values in a dictionary
values_dict = {
    "group": specific_values.get("Group:", "Not Found"),
    "spec_level": text_lines[10],
    "contract_start": specific_values.get("Incurred From:", "Not Found"),
    "contract_end": specific_values.get("To:", "Not Found"),
    "plan_start_date": specific_values.get("Incurred From:", "Not Found"),
    "incurred": incurred,
    "paid": paid,
    "min_attachment_point": text_lines[8],
    "single": text_lines[54],
    "emp+wife": text_lines[42],
    "emp_child": text_lines[48],
    "family": text_lines[36],
}

# Assuming there's a date column to split like before
"""date_value = values_dict.get("contract_start")
if date_value and "To:" in date_value:
    date_parts = date_value.split('To:')
    if len(date_parts) == 2:
        #values_dict['contract_start'] = date_parts[0].strip()
        #values_dict['contract_end'] = date_parts[1].strip()
    else:
        print("Unexpected date format in the 'From' value")"""

# Display the dictionary with extracted values
print("Extracted Specific Values in Dictionary Form:")
print(values_dict)


# In[ ]:





# In[166]:


df=dataframes['table_1']
df


# In[167]:


df = dataframes['table_1']
values_dict['spec_level'] = df.iloc[:1,4:5]


# In[168]:


values_dict['spec_level']
df


# In[169]:


spec_deductible_str = df.iloc[0, 4]
print(spec_deductible_str)

if isinstance(spec_deductible_str, bytes):
    spec_deductible_str = spec_deductible_str.decode('utf-8')  # Decode to string

# Use regular expression to extract the numeric value
match = re.search(r'\d{1,3}(?:,\d{3})*(?:\.\d{2})?', spec_deductible_str)

if match:
    specific_value = match.group(0)
    values_dict['spec_level'] = specific_value

print(values_dict)


# In[170]:


spec_deductible_str = df.iloc[18, 0]
print(spec_deductible_str)

# Split the string by spaces to get individual components
parts = spec_deductible_str.split()

# Assuming the third part is the value we want
if len(parts) > 2:
    third_value = parts[2]  # Get the third component

    # Use regular expression to extract the numeric value from this component
    match = re.search(r'\d{1,3}(?:,\d{3})*(?:\.\d{2})?', third_value)

    if match:
        specific_value = match.group(0)
        values_dict['min_attachment_point'] = specific_value

print(values_dict)


# In[171]:


new_headers = df.iloc[10]
table1 = df.iloc[11:15,:6]
#main_table = main_table.iloc[5:17,:]
table1.columns = new_headers


# In[172]:


table1


# In[173]:


import pandas as pd

# Sample data similar to your original DataFrame

df = pd.DataFrame(table1)

# Split the 'Year Month Tier' column into separate columns
df[['Year', 'Month', 'Tier']] = df['Year Month Tier'].str.split(expand=True, n=2)

# Split the 'Zip Thru Count Factor Attachment Point' column into separate columns
df[['Count', 'Factor', 'Attachment Point']] = df['Zip Thru Count Factor Attachment Point'].str.split(expand=True, n=3)

# Drop the original mixed columns
df.drop(columns=['Year Month Tier', 'Plan ID Age From Age Thru Zip From', 'Zip Thru Count Factor Attachment Point'], inplace=True, errors='ignore')

# Convert the split columns to their appropriate data types
#df['Zip'] = pd.to_numeric(df['Zip'], errors='coerce')
df['Count'] = df['Count'].str.replace(',', '').astype(float, errors='ignore')
df['Factor'] = df['Factor'].str.replace(',', '').astype(float, errors='ignore')
df['Attachment Point'] = df['Attachment Point'].str.replace(',', '').astype(float, errors='ignore')

# Print the resulting DataFrame
print(df)


# In[174]:


table1 = df


# In[175]:


table1


# In[176]:


values_dict['Enrollment member- EE']  = table1.iloc[3, 6]
values_dict['Enrollment member - ES'] = table1.iloc[1, 6]
values_dict['Enrollment member - EC'] = table1.iloc[2, 6]
values_dict['Enrollment member- Fam'] = table1.iloc[0, 6]
values_dict['Agg Factors - EE']  = table1.iloc[3, 7]
values_dict['Agg Factors - ES'] = table1.iloc[1, 7]
values_dict['Agg Factors - EC'] = table1.iloc[2, 7]
values_dict['Agg Factors - Fam'] = table1.iloc[0, 7]


# In[177]:


table1.columns
values_dict


# In[178]:


table2= dataframes['table_1']
table2


# In[179]:


new_headers = table2.iloc[17]
table2 = table2.iloc[18:19]
#main_table = main_table.iloc[5:17,:]
table2.columns
table2.columns = new_headers
table2


# In[180]:


new_column_names = {
    'Claims Paid': ['Medical Claims Paid', 'Rx Claims Paid']
}

# Update column names to avoid repetition
current_column_names = table2.columns.tolist()
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
table2.columns = updated_column_names


# In[181]:


table2.columns


# In[182]:


import pandas as pd

# Sample data similar to your original DataFrame

df = pd.DataFrame(table2)

# Split the 'Year Month Tier' column into separate columns
df[['Year', 'Month', 'Point']] = df['Year Month Point'].str.split(expand=True, n=2)

# Split the 'Zip Thru Count Factor Attachment Point' column into separate columns
df[['Medical Claims Paid', 'Rx Claims Paid', 'Reimbursed']] = df['Claims Paid Claims Paid Reimbursed'].str.split(expand=True, n=2)

df[['Claims Pending', 'Deductible', 'Spec Deductible']] = df['Claims Pending Deductible Spec Deductible'].str.split(expand=True, n=2)

# Drop the original mixed columns
df.drop(columns=['Year Month Point', 'Claims Paid Claims Paid Reimbursed','Claims Pending Deductible Spec Deductible'], inplace=True, errors='ignore')

# Convert the split columns to their appropriate data types
#df['Zip'] = pd.to_numeric(df['Zip'], errors='coerce')
#df['Count'] = df['Count'].str.replace(',', '').astype(float, errors='ignore')
#df['Factor'] = df['Factor'].str.replace(',', '').astype(float, errors='ignore')
#df['Attachment Point'] = df['Attachment Point'].str.replace(',', '').astype(float, errors='ignore')

# Print the resulting DataFrame
print(df)


# In[ ]:





# In[183]:


table2 = df


# In[184]:


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
master_df_JPFarley = pd.DataFrame(columns=columns)

# Print the DataFrame to verify
print("DataFrame with specified columns:")
print(master_df_JPFarley)


# In[185]:


print(table2.columns)
print(table1.columns)
print(values_dict)


# In[ ]:





# In[186]:


table2['Medical Claims Paid'] = pd.to_numeric(table2['Medical Claims Paid'].str.replace(',', ''), errors='coerce').fillna(0)
table2['Rx Claims Paid'] = pd.to_numeric(table2['Rx Claims Paid'].str.replace(',', ''), errors='coerce').fillna(0)
table2['Total'] = pd.to_numeric(table2['Total'].str.replace(',', ''), errors='coerce').fillna(0)
table2['SSpec Deductible'] = pd.to_numeric(table2['Spec Deductible'].str.replace(',', ''), errors='coerce').fillna(0)


# In[187]:


master_df_JPFarley['Month']= table2['Month']
master_df_JPFarley['Enrollment - EE']= values_dict["Enrollment member- EE"]
master_df_JPFarley['Enrollment - ES']= values_dict["Enrollment member - ES"]
master_df_JPFarley['Enrollment - EC']= values_dict["Enrollment member - EC"]
master_df_JPFarley['Enrollment - Fam']= values_dict['Enrollment member- Fam']
master_df_JPFarley['Monthly Attachment']= table2['Point']

#master_df_JPFarley['Cumlative Attachment']= main_table['Attachment Point']

master_df_JPFarley['Monthly Medical']= table2['Medical Claims Paid']

master_df_JPFarley['Monthly RX']= table2['Rx Claims Paid']

master_df_JPFarley['Monthly Total']= table2['Medical Claims Paid'] + table2['Rx Claims Paid']
master_df_JPFarley['Total Medical']= table2['Medical Claims Paid'].cumsum()

master_df_JPFarley['Total RX']= table2['Rx Claims Paid'].cumsum()

master_df_JPFarley['Total Paid']= table2['Medical Claims Paid'] + table2['Rx Claims Paid']

master_df_JPFarley['Total Attchment (Running)']= table2['Point'].cumsum()

#master_df_JPFarley['Total Claims (Running)']= main_table['YTD Paid Subject To Loss Fund']

master_df_JPFarley['Spec Claim amount']= table2['Reimbursed']
master_df_JPFarley['Spec Total (running)']= table2['Reimbursed'].cumsum()
#master_df_JPFarley['Not Covered (Monthly)']= main_table['Not Covered']

#master_df_JPFarley['Group Id']= values_dict['group']

master_df_JPFarley['Contract Start']= values_dict['contract_start']
master_df_JPFarley['Contract End']= values_dict['contract_end']
master_df_JPFarley['Plan Start Date']= values_dict['plan_start_date']
master_df_JPFarley['Min Attachment Point']= values_dict['min_attachment_point']
master_df_JPFarley['Spec Level']= values_dict['spec_level']
master_df_JPFarley['Agg Factors EE']= values_dict['single']
master_df_JPFarley['Agg Factors ES']= values_dict['emp+wife']
master_df_JPFarley['Agg Factors EC']= values_dict['emp_child']
master_df_JPFarley['Agg Factors Fam']= values_dict['family']

master_df_JPFarley['Incurred'] = values_dict['incurred']

master_df_JPFarley['Paid'] = values_dict['paid']


# In[188]:


master_df_JPFarley


# In[189]:


# Function to remove dollar signs and convert to float
def convert_to_float(value):
    # Check if the value is a string and contains a dollar sign
    if isinstance(value, str) and '$' in value:
        # Remove the dollar sign and commas, then convert to float
        return float(value.replace('$', '').replace(',', ''))
    return value

# Apply the conversion to all elements in the DataFrame
master_df_JPFarley = master_df_JPFarley.applymap(convert_to_float)


# In[191]:


master_df_JPFarley['Total Medical']


# In[135]:


master_df_JPFarley.to_csv(r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\master_df\master_df_JPFarley.csv")


# In[ ]:





# In[225]:


df1 = dataframes['table_1']
df2 = dataframes['table_2']
df3 = dataframes['table_3']
df4 = dataframes['table_4']
df5 = dataframes['table_5']
final_df = pd.concat([df1,df2,df3,df4,df5], ignore_index=True)


# In[157]:


df2


# In[ ]:




