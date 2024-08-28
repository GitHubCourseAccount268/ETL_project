#!/usr/bin/env python
# coding: utf-8

# In[31]:


import tabula
import fitz  # PyMuPDF
import pandas as pd
import re

def extract_tables_from_pdf(pdf_path):
    # Use tabula to extract tables from the PDF
    tables = tabula.read_pdf(pdf_path, pages="all", multiple_tables=True, lattice=False)
    return tables

def extract_text_from_pdf(pdf_path):
    # Use PyMuPDF to extract text from the PDF
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
        
    return text

def extract_specific_values(text, labels):
    # Extract specific values following given labels
    extracted_data = {}
    for label in labels:
        pattern = re.compile(rf"{label}\s*(.*?)(?:\n|$)", re.IGNORECASE)
        match = pattern.search(text)
        if match:
            extracted_data[label] = match.group(1).strip()
    return extracted_data

def parse_agg_factors(label, agg_factors):
    # Parse aggregate factors from a string
    parsed_factors = {}
    pattern = re.compile(r"\$(\d+\.\d{2})\s*\$(\d+\.\d{2})\s*\$(\d+\.\d{2})\s*\$(\d+\.\d{2})")
    match = pattern.search(agg_factors)
    if match:
        values = list(map(float, match.groups()))
        parsed_factors = {
            'EE': values[0],
            'EE+SP': values[1],
            'EE+CH': values[2],
            'Fam': values[3]
        }
    return parsed_factors

def parse_effective_date(effective_str):
    # Parse effective date from a string
    pattern = re.compile(r"Date of Plan:\s*(\d{1,2}/\d{1,2}/\d{4})")
    match = pattern.search(effective_str)
    if match:
        return match.group(1)
    return "Not Found"

def parse_contract_values(contract_str):
    # Parse contract values allowing optional spaces around the slash
    pattern = re.compile(r"(\d+)\s*/\s*(\d+)")
    match = pattern.search(contract_str)
    if match:
        incurred, paid = match.groups()
        return int(incurred), int(paid)
    return None, None 

pdf_path = r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\pdf\Edison\JCM330 Agg.pdf"
labels = ["Paid From","Attachment Min", "Contract Type", "Group Name", "Specific Deductible", "Employee Only", "Employee + Children/Dependent", "Employee + Spouse", "Family"]

# Extracting tables from the PDF
tables = extract_tables_from_pdf(pdf_path)

# Storing tables as separate DataFrames
dataframes = {}
for i, table in enumerate(tables):
    df_name = f'table_{i + 1}'
    dataframes[df_name] = pd.DataFrame(table)

# Extracting text from the PDF
text = extract_text_from_pdf(pdf_path)

text_lines = text.splitlines()
for index, line in enumerate(text_lines):
    print(f"Index {index}: {line}")

# Extracting specific values
specific_values = extract_specific_values(text, labels)

# Parse the 'Agg Factors' and 'Effective' fields
agg_factors_str = specific_values.get("MEDA", "")
parsed_factors = parse_agg_factors("MEDA", agg_factors_str)
specific_values.update(parsed_factors)

# Extract and parse dates and contract values
effective_date_str = specific_values.get("Paid From", "")
plan_start_date = parse_effective_date(effective_date_str)

contract_str = specific_values.get("Contract Type", "")
incurred, paid = parse_contract_values(contract_str)

contract_str = text_lines[52]
incurred, paid = parse_contract_values(contract_str)

# Store specific extracted values in a dictionary
values_dict = {
    "group": specific_values.get("Group Name", "Not Found"),
    "spec_level": text_lines[41],
    "Plan Year": specific_values.get("Specific Deductible", "Not Found"),
    "incurred": incurred,
    "paid": paid,
    "min_attachment_point": text_lines[37],
    "incurred": incurred,
    "paid": paid,
    "single": text_lines[18],
    "emp+wife": text_lines[26],
    "emp_child": text_lines[22],
    "family": text_lines[30],
}

# Splitting 'Plan Year' into start and end dates
date_value = values_dict.get("Plan Year")
if date_value and "To:" in date_value:
    date_parts = date_value.split('To:')
    if len(date_parts) == 2:
        values_dict['contract_start'] = date_parts[0].strip()
        values_dict['contract_end'] = date_parts[1].strip()
    else:
        print("Unexpected date format in the 'Plan Year' value")
values_dict['plan_start_date'] = values_dict.get('contract_start', 'Not Found')

# Display the dictionary with extracted values
print("Extracted Specific Values in Dictionary Form:")
print(values_dict)


# In[32]:


table1=dataframes['table_1']
table2 = dataframes['table_2']
table2


# In[33]:


new_columns = table2.iloc[3]
table2 = table2.iloc[5:18,:]
table2.columns = new_columns
table2


# In[34]:


table2.columns


# In[35]:


import pandas as pd

# Sample data similar to your mixed DataFrame


df = pd.DataFrame(table2)

# Split the first mixed column into separate columns
df[['EE', 'EE/SP']] = df['EE EE/SP'].str.split(expand=True, n=1)
df[['Pending', 'Deductible']] = df['Pending Deductible'].str.split(expand=True, n=1)
df[['Family', 'Enrollment Total']] = df['Family Total'].str.split(expand=True, n=1)
df
# Remove the original mixed columns
df.drop(columns=['EE EE/SP', 'Pending Deductible', 'Family Total'], inplace=True)

print(df)


# In[36]:


table2 = df
table2


# In[37]:


new_column_names = [ 'Month-Year', 'EE/Chd',  'Attachment Point', 'Medical Claims', 'Rx Paid',  'Eligible claims', 'Specific Claims reimbursed',  'blank1', 'Specific Deductible', 'Agg Spec Deductible', 'Aggregate total', 'Loss Ration','EE','EE/SP','Specific Claims pending', 'spec deductible', 'Family', "enrollmet total"]
table2.columns = new_column_names


# In[38]:


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
master_df_Edison = pd.DataFrame(columns=columns)

# Print the DataFrame to verify
print("DataFrame with specified columns:")
print(master_df_Edison)


# In[39]:


table2.columns


# In[40]:


table2['Medical Claims'] = pd.to_numeric(table2['Medical Claims'].str.replace(',', ''), errors='coerce').fillna(0)
table2['Rx Paid'] = pd.to_numeric(table2['Rx Paid'].str.replace(',', ''), errors='coerce').fillna(0)
table2['Eligible claims'] = pd.to_numeric(table2['Eligible claims'].str.replace(',', ''), errors='coerce').fillna(0)

table2['Attachment Point'] = pd.to_numeric(table2['Attachment Point'].str.replace(',', ''), errors='coerce').fillna(0)
table2['Specific Claims reimbursed'] = pd.to_numeric(table2['Specific Claims reimbursed'].str.replace(',', ''), errors='coerce').fillna(0)


# In[41]:


table2


# In[42]:


master_df_Edison['Month']= table2['Month-Year']
master_df_Edison['Enrollment - EE']= table2["EE"]
master_df_Edison['Enrollment - ES']= table2["EE/SP"]
master_df_Edison['Enrollment - EC']= table2["EE/Chd"]
master_df_Edison['Enrollment - Fam']= table2['Family']
master_df_Edison['Monthly Attachment']= table2['Attachment Point']

master_df_Edison['Cumlative Attachment']= table2['Attachment Point'].cumsum()

master_df_Edison['Monthly Medical']= table2['Medical Claims']

master_df_Edison['Monthly RX']= table2['Rx Paid']

master_df_Edison['Monthly Total']= table2['Eligible claims']
master_df_Edison['Total Medical']= table2['Medical Claims'].cumsum()

master_df_Edison['Total RX']= table2['Rx Paid'].cumsum()

master_df_Edison['Total Paid']= table2['Eligible claims'].cumsum()

master_df_Edison['Total Attchment (Running)']= table2['Attachment Point'].cumsum()

master_df_Edison['Total Claims (Running)']= table2['Eligible claims'].cumsum()

master_df_Edison['Spec Claim amount']= table2['Specific Claims reimbursed']
master_df_Edison['Spec Total (running)']= table2['Specific Claims reimbursed'].cumsum()
#master_df_Edison['Not Covered (Monthly)']= table2[' Not Covered']
#master_df_Edison['Spec claimant ID']= table2['REL']
#master_df_Edison['Spec Claimant Amount']= table2['AMT OVER SPEC']

master_df_Edison['Group Id']= values_dict['group']

#master_df_Edison['Contract Start']= values_dict['contract_start']
#master_df_Edison['Contract End']= values_dict['contract_end']
#master_df_Edison['Contract Start']= values_dict['plan_start_date']
master_df_Edison['Min Attachment Point']= values_dict['min_attachment_point']
master_df_Edison['Spec Level']= values_dict['spec_level']
master_df_Edison['Agg Factors EE']= values_dict['single']
master_df_Edison['Agg Factors ES']= values_dict['emp+wife']
master_df_Edison['Agg Factors EC']= values_dict['emp_child']
master_df_Edison['Agg Factors Fam']= values_dict['family']
master_df_Edison['Incurred'] = values_dict['incurred']

master_df_Edison['Paid'] = values_dict['paid']


# In[43]:


# Function to remove dollar signs and convert to float
def convert_to_float(value):
    # Check if the value is a string and contains a dollar sign
    if isinstance(value, str) and '$' in value:
        # Remove the dollar sign and commas, then convert to float
        return value.replace('$', '').replace(',', '')
    return value

# Apply the conversion to all elements in the DataFrame
master_df_Edison = master_df_Edison.applymap(convert_to_float)


# In[45]:


master_df_Edison.to_csv(r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\master_df\master_df_Edison.csv")


# In[ ]:




