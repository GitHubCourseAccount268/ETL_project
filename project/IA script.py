#!/usr/bin/env python
# coding: utf-8

# In[91]:


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
        #print(text)
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

def extract_meda_values(text):
    # Regular expression pattern to match "MEDA" followed by four dollar values
    pattern = re.compile(r"MEDA\s*\$([\d,]+\.\d{2})\s*\$([\d,]+\.\d{2})\s*\$([\d,]+\.\d{2})\s*\$([\d,]+\.\d{2})", re.IGNORECASE)
    
    # Search for the pattern in the text
    match = pattern.search(text)
    
    if match:
        # Extract the four values and convert them to floats
        values = list(map(lambda x: float(x.replace(',', '')), match.groups()))
        return {
            'EE': values[0],
            'EE+SP': values[1],
            'EE+CH': values[2],
            'Fam': values[3]
        }
    
    # Return None or an empty dictionary if no match is found
    return None

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

pdf_path = r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\pdf\Independence administrators\True Captive - Aggregate Reports - 0524.pdf"
labels = ["Policy Period :","Monthly Minimum:", "Contract Type", "Group Name", "Specific Deductible", "Employee Only", "Employee + Children/Dependent", "Employee + Spouse", "Family"]

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

extracted_meda_values = extract_meda_values(text)
print(extracted_meda_values)

# Extracting specific values
specific_values = extract_specific_values(text, labels)

# Parse the 'Agg Factors' and 'Effective' fields
agg_factors_str = specific_values.get("MEDA", "")
parsed_factors = parse_agg_factors("MEDA", agg_factors_str)
specific_values.update(parsed_factors)

# Extract and parse dates and contract values
effective_date_str = specific_values.get("Policy Period :", "")
plan_start_date = parse_effective_date(effective_date_str)

contract_str = specific_values.get("Contract Type", "")
incurred, paid = parse_contract_values(contract_str)


contract_str = text_lines[8]
incurred, paid = parse_contract_values(contract_str)

# Store specific extracted values in a dictionary
values_dict = {
    "group": specific_values.get("Group Name", "Not Found"),
    "spec_level": specific_values.get("Specific Deductible", "Not Found"),
    "Plan Year": specific_values.get("Policy Period :", "Not Found"),
    "incurred": incurred,
    "paid": paid,
    "min_attachment_point": specific_values.get("Monthly Minimum:", "Not Found"),
    "single": extracted_meda_values.get('EE', "Not Found"),
    "emp+wife": extracted_meda_values.get("EE+SP", "Not Found"),
    "emp_child": extracted_meda_values.get("EE+CH", "Not Found"),
    "family": extracted_meda_values.get("Fam", "Not Found"),
}

# Splitting 'Plan Year' into start and end dates
date_value = values_dict.get("Plan Year")
if date_value and "-" in date_value:
    date_parts = date_value.split('-')
    if len(date_parts) == 2:
        values_dict['contract_start'] = date_parts[0].strip()
        values_dict['contract_end'] = date_parts[1].strip()
    else:
        print("Unexpected date format in the 'Plan Year' value")
values_dict['plan_start_date'] = values_dict.get('contract_start', 'Not Found')


# Display the dictionary with extracted values
print("Extracted Specific Values in Dictionary Form:")
print(values_dict)


# In[92]:


table1 = dataframes['table_1']


# In[93]:


table1


# In[94]:


new_cols = table1.iloc[11]
table1 = table1.iloc[13:17]
table1.columns = new_cols
table1


# In[95]:


table1.columns


# In[96]:


import pandas as pd

# Sample data similar to your mixed DataFrame


df = pd.DataFrame(table1)

# Split the first mixed column into separate columns
df[['Month', 'EE', 'ES', 'EC', 'FF', 'Units', 'Monthly attch.', 'Cummulative attch.']] = df['Month EE ES EC FF Units Monthly Cummulative'].str.split(expand=True, n=7)
df[['Medical', 'Rx']] = df['Medical Rx'].str.split(expand=True, n=1)
df[['Monthly Net', 'Cummulative Net']] = df['Net Net'].str.split(expand=True, n=1)
df
# Remove the original mixed columns
df.drop(columns=['Month EE ES EC FF Units Monthly Cummulative', 'Medical Rx', 'Net Net'], inplace=True)

print(df)


# In[97]:


table1 = df


# In[98]:


# Function to remove dollar signs and convert to float
def convert_to_float(value):
    # Check if the value is a string and contains a dollar sign
    if isinstance(value, str) and '$' in value:
        # Remove the dollar sign and commas, then convert to float
        return value.replace('$', '').replace(',', '')
    return value

# Apply the conversion to all elements in the DataFrame
table1 = table1.applymap(convert_to_float)


# In[99]:


table1


# In[ ]:





# In[100]:


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
master_df_IA = pd.DataFrame(columns=columns)

# Print the DataFrame to verify
print("DataFrame with specified columns:")
print(master_df_IA)


# In[101]:


table1.columns


# In[102]:


table1['Medical'] = pd.to_numeric(table1['Medical'].str.replace(',', ''), errors='coerce').fillna(0)
table1['Rx'] = pd.to_numeric(table1['Rx'].str.replace(',', ''), errors='coerce').fillna(0)
table1['Total'] = pd.to_numeric(table1['Total'].str.replace(',', ''), errors='coerce').fillna(0)

table1['Covered'] = pd.to_numeric(table1['Covered'].str.replace(',', ''), errors='coerce').fillna(0)
table1['Specific'] = pd.to_numeric(table1['Specific'].str.replace(',', ''), errors='coerce').fillna(0)


# In[103]:


master_df_IA['Month']= table1['Month']
master_df_IA['Enrollment - EE']= table1["EE"]
master_df_IA['Enrollment - ES']= table1["ES"]
master_df_IA['Enrollment - EC']= table1["EC"]
master_df_IA['Enrollment - Fam']= table1['FF']
master_df_IA['Monthly Attachment']= table1['Monthly attch.']

master_df_IA['Cumlative Attachment']= table1['Cummulative attch.']

master_df_IA['Monthly Medical']= table1['Medical']

master_df_IA['Monthly RX']= table1['Rx']

#master_df_IA['Monthly Total']= table1['Monthly Net']
master_df_IA['Total Medical']= table1['Medical'].cumsum()

master_df_IA['Total RX']= table1['Rx'].cumsum()

master_df_IA['Total Paid']= table1['Total'].cumsum()

master_df_IA['Total Attchment (Running)']= table1['Cummulative attch.']

master_df_IA['Total Claims (Running)']= table1['Monthly Net']

master_df_IA['Spec Claim amount']= table1['Specific']
master_df_IA['Spec Total (running)']= table1['Specific'].cumsum()
master_df_IA['Not Covered (Monthly)']= table1['Covered']
master_df_IA['Not Covered (Running)']= table1['Covered'].cumsum()

#master_df_IA['Spec claimant ID']= table1['REL']
#master_df_IA['Spec Claimant Amount']= table1['AMT OVER SPEC']

master_df_IA['Group Id']= values_dict['group']

master_df_IA['Contract Start']= values_dict['contract_start']
master_df_IA['Contract End']= values_dict['contract_end']
master_df_IA['Contract Start']= values_dict['plan_start_date']
master_df_IA['Min Attachment Point']= values_dict['min_attachment_point']
master_df_IA['Spec Level']= values_dict['spec_level']
master_df_IA['Agg Factors EE']= values_dict['single']
master_df_IA['Agg Factors ES']= values_dict['emp+wife']
master_df_IA['Agg Factors EC']= values_dict['emp_child']
master_df_IA['Agg Factors Fam']= values_dict['family']

master_df_IA['Incurred'] = values_dict['incurred']

master_df_IA['Paid'] = values_dict['paid']

master_df_IA['Plan Start Date'] = values_dict['plan_start_date']


# In[104]:


# Function to remove dollar signs and convert to float
def convert_to_float(value):
    # Check if the value is a string and contains a dollar sign
    if isinstance(value, str) and '$' in value:
        # Remove the dollar sign and commas, then convert to float
        return value.replace('$', '').replace(',', '')
    return value

# Apply the conversion to all elements in the DataFrame
master_df_IA = master_df_IA.applymap(convert_to_float)


# In[105]:


master_df_IA.to_csv(r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\master_df\master_df_IA.csv")


# In[ ]:




