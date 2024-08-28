#!/usr/bin/env python
# coding: utf-8

# In[37]:


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

pdf_path = r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\pdf\Luminare\Monthly Aggregate Report.pdf"
labels = ["Minimum Attachment Point:", "Contract Year", "Group Name", "Specific Deductible:", "Single", "EE+ Chifd(ren)", "EE+ Spouse", "Family"]

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

#extracted_meda_values = extract_meda_values(text)
#print(extracted_meda_values)

# Extracting specific values
specific_values = extract_specific_values(text, labels)

# Parse the 'Agg Factors' and 'Effective' fields
agg_factors_str = specific_values.get("MEDA", "")
parsed_factors = parse_agg_factors("MEDA", agg_factors_str)
specific_values.update(parsed_factors)

# Extract and parse dates and contract values
effective_date_str = text_lines[9]
plan_start_date = parse_effective_date(effective_date_str)

contract_str = specific_values.get("Contract Type", "")
incurred, paid = parse_contract_values(contract_str)

# Store specific extracted values in a dictionary
values_dict = {
    "group": specific_values.get("Group Name", "Not Found"),
    "spec_level": text_lines[17],
    "Plan Year": specific_values.get("Contract Year:", "Not Found"),
    "incurred": specific_values.get("Incurred:", "Not Found"),
    "paid": specific_values.get("Paid:", "Not Found"),
    "min_attachment_point": text_lines[33],
    "single": text_lines[26],
    "emp+wife": text_lines[40],
    "emp_child": text_lines[41],
    "family": text_lines[42],
}

# Splitting 'Plan Year' into start and end dates
date_value = text_lines[9]
if date_value and "through" in date_value:
    date_parts = date_value.split('through')
    if len(date_parts) == 2:
        values_dict['contract_start'] = date_parts[0].strip()
        values_dict['contract_end'] = date_parts[1].strip()
    else:
        print("Unexpected date format in the 'Plan Year' value")
values_dict['plan_start_date'] = values_dict.get('contract_start', 'Not Found')

Incurred_value = text_lines[28]
if Incurred_value and "through" in date_value:
    date_parts = Incurred_value.split('through')
    if len(date_parts) == 2:
        values_dict['incurred'] = date_parts[0].strip()
        #values_dict['contract_end'] = date_parts[1].strip()
    else:
        print("Unexpected date format in the 'Plan Year' value")


paid_value = text_lines[28]
if paid_value and "through" in date_value:
    date_parts = paid_value.split('through')
    if len(date_parts) == 2:
        values_dict['paid'] = date_parts[0].strip()
        #values_dict['contract_end'] = date_parts[1].strip()
    else:
        print("Unexpected date format in the 'Plan Year' value")

# Display the dictionary with extracted values
print("Extracted Specific Values in Dictionary Form:")
print(values_dict)


# In[38]:


table1 = dataframes['table_1']
table1


# In[39]:


#new_cols = table1.iloc[2]
new_col_name = ['Month',	'Single',	'Spouse',	'Child(ren)',	'Family',	'Monthly agg. Deductible',	'YTD agg Deductible',	'medical Claims',	'other Paid (1)',	'Rx Paid Claims',	'gross paid claims Included',	'Excluded Aggregate (2)',	'Specific',	'Monthly net agg Paid Claims',	'Expected Claims']
table1 = table1.iloc[3:]
table1.columns = new_col_name
table1


# In[40]:


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
master_df_Luminare = pd.DataFrame(columns=columns)

# Print the DataFrame to verify
print("DataFrame with specified columns:")
print(master_df_Luminare)


# In[41]:


table1['medical Claims'] = pd.to_numeric(table1['medical Claims'].str.replace(',', ''), errors='coerce').fillna(0)
table1['Rx Paid Claims'] = pd.to_numeric(table1['Rx Paid Claims'].str.replace(',', ''), errors='coerce').fillna(0)
table1['gross paid claims Included'] = pd.to_numeric(table1['gross paid claims Included'].str.replace(',', ''), errors='coerce').fillna(0)
table1['Specific'] = pd.to_numeric(table1['Specific'].str.replace(',', ''), errors='coerce').fillna(0)
table1['Excluded Aggregate (2)'] = pd.to_numeric(table1['Excluded Aggregate (2)'].str.replace(',', ''), errors='coerce').fillna(0)


# In[42]:


table1.columns


# In[43]:


master_df_Luminare['Month']= table1['Month']
master_df_Luminare['Enrollment - EE']= table1["Single"]
master_df_Luminare['Enrollment - ES']= table1["Spouse"]
master_df_Luminare['Enrollment - EC']= table1["Child(ren)"]
master_df_Luminare['Enrollment - Fam']= table1['Family']
master_df_Luminare['Monthly Attachment']= table1['Monthly agg. Deductible']

master_df_Luminare['Cumlative Attachment']= table1['YTD agg Deductible']

master_df_Luminare['Monthly Medical']= table1['medical Claims']

master_df_Luminare['Monthly RX']= table1['Rx Paid Claims']

master_df_Luminare['Monthly Total']= table1['gross paid claims Included']
master_df_Luminare['Total Medical']= table1['medical Claims'].cumsum()

master_df_Luminare['Total RX']= table1['Rx Paid Claims'].cumsum()

master_df_Luminare['Total Paid']= table1['gross paid claims Included'].cumsum()

#master_df_Luminare['Total Attchment (Running)']= table1['min. attach. pt']

#master_df_Luminare['Total Claims (Running)']= table1['Monthly Net']

master_df_Luminare['Spec Claim amount']= table1['Specific']
master_df_Luminare['Spec Total (running)']= table1['Specific'].cumsum()
master_df_Luminare['Not Covered (Monthly)']= table1['Excluded Aggregate (2)']
master_df_Luminare['Not Covered (Running)']= table1['Excluded Aggregate (2)'].cumsum()
#master_df_Luminare['Spec claimant ID']= table1['REL']
#master_df_Luminare['Spec Claimant Amount']= table1['AMT OVER SPEC']

master_df_Luminare['Group Id']= values_dict['group']

master_df_Luminare['Contract Start']= values_dict['contract_start']
master_df_Luminare['Contract End']= values_dict['contract_end']
master_df_Luminare['Plan Start Date']= values_dict['plan_start_date']
master_df_Luminare['Min Attachment Point']= values_dict['min_attachment_point']
master_df_Luminare['Spec Level']= values_dict['spec_level']
master_df_Luminare['Agg Factors EE']= values_dict['single']
master_df_Luminare['Agg Factors ES']= values_dict['emp+wife']
master_df_Luminare['Agg Factors EC']= values_dict['emp_child']
master_df_Luminare['Agg Factors Fam']= values_dict['family']
master_df_Luminare['Incurred'] = values_dict['incurred']
master_df_Luminare['Paid'] = values_dict['paid']


# In[44]:


# Function to remove dollar signs and convert to float
def convert_to_float(value):
    # Check if the value is a string and contains a dollar sign
    if isinstance(value, str) and '$' in value:
        # Remove the dollar sign and commas, then convert to float
        return value.replace('$', '').replace(',', '')
    return value

# Apply the conversion to all elements in the DataFrame
table1 = table1.applymap(convert_to_float)


# In[45]:


master_df_Luminare['Total RX']


# In[47]:


master_df_Luminare.to_csv(r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\master_df\master_df_luminare.csv")


# In[ ]:




