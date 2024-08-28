#!/usr/bin/env python
# coding: utf-8

# In[20]:


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

pdf_path = r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\pdf\90 Degrees DBA entrust\True Captive - Aggregate Reports - 1223.pdf"
labels = ["Policy Period", "Contract Type", "Group Name", "MEDA"]

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
effective_date_str = specific_values.get("Policy Period", "")
plan_start_date = parse_effective_date(effective_date_str)

contract_str = specific_values.get("Contract Type", "")
incurred, paid = parse_contract_values(contract_str)

# Store specific extracted values in a dictionary
values_dict = {
    "group": specific_values.get("Group Name", "Not Found"),
    "spec_level": specific_values.get("Spec Deductible", "Not Found"),
    "Plan Year": specific_values.get("Policy Period", "Not Found"),
    "incurred": incurred,
    "paid": paid,
    "single": text_lines[11],
    "emp+wife": text_lines[12],
    "emp_child": text_lines[13],
    "family": text_lines[14],
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


# In[21]:


table1 = dataframes['table_1']
#table2 = dataframes['table_2']


# In[22]:


#new_headers = table1.iloc[3]
table1 = table1.iloc[0:10,:]
#table1.columns = new_headers


# In[23]:


table1


# In[24]:


import pandas as pd

# Sample DataFrame similar to your `table1`

# The first row to be added
missed_row_jan = [
    'Jan-23 9', '1', '2', '5', '17', '$9,848.32', '$9,848.32', '11,988.60',
    '$11,988.60', '$11,706.48', '$0.00', '$282.12', '$282.12', '-$9,566.20'
]

# The second row as the column names of table1
missed_row_feb = list(table1.columns)

# Convert missed_row_jan and missed_row_feb into DataFrames
missed_row_jan_df = pd.DataFrame([missed_row_jan], columns=table1.columns)
missed_row_feb_df = pd.DataFrame([missed_row_feb], columns=table1.columns)

# Append both rows at the start of the DataFrame
table1 = pd.concat([missed_row_jan_df, missed_row_feb_df, table1]).reset_index(drop=True)

print(table1)


# In[25]:


new_column_names = [ 'Month EE', 'ES', 'EC', 'FF', 'Units Covered', 'Monthly attch pt', 'Cummulative attch pt',  'Medical & Rx', 'Total', ' Not Covered',  'Over Specific',  'Monthly Net', 'Cummulative Net', 'Exces']
table1.columns=new_column_names


# In[26]:


table1


# In[27]:


import pandas as pd

# Sample data similar to your mixed DataFrame


df = pd.DataFrame(table1)

# Split the first mixed column into separate columns
df[['Month', 'EE']] = df['Month EE'].str.split(expand=True, n=1)

# Remove the original mixed columns
df.drop(columns=['Month EE'], inplace=True)

print(df)


# In[28]:


table1 =df


# In[29]:


table1


# In[30]:


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
master_df_DBA = pd.DataFrame(columns=columns)

# Print the DataFrame to verify
print("DataFrame with specified columns:")
print(master_df_DBA)


# In[31]:


# Function to remove dollar signs and convert to float
def convert_to_float(value):
    # Check if the value is a string and contains a dollar sign
    if isinstance(value, str) and '$' in value:
        # Remove the dollar sign and commas, then convert to float
        return value.replace('$', '').replace(',', '')
    return value

# Apply the conversion to all elements in the DataFrame
table1 = table1.applymap(convert_to_float)


# In[40]:


table1['Over Specific'] = pd.to_numeric(table1['Over Specific'].str.replace(',', ''), errors='coerce').fillna(0)


# In[41]:


table1.columns


# In[46]:


master_df_DBA['Month']= table1['Month']
master_df_DBA['Enrollment - EE']= table1["EE"]
master_df_DBA['Enrollment - ES']= table1["ES"]
master_df_DBA['Enrollment - EC']= table1["EC"]
master_df_DBA['Enrollment - Fam']= table1['FF']
master_df_DBA['Monthly Attachment']= table1['Monthly attch pt']

master_df_DBA['Cumlative Attachment']= table1['Cummulative attch pt']

#master_df_DBA['Monthly Medical']= table1['Medical']

#master_df_DBA['Monthly RX']= table1['Pharamacy']

master_df_DBA['Monthly Total']= table1['Total']
#master_df_DBA['Total Medical']= table['Total Medical']

#master_df_DBA['Total RX']= table['Total RX']

master_df_DBA['Total Paid']= table1['Total']

master_df_DBA['Total Attchment (Running)']= table1['Cummulative attch pt']

master_df_DBA['Total Claims (Running)']= table1['Total']

master_df_DBA['Spec Claim amount']= table1['Over Specific']
master_df_DBA['Spec Total (running)']= table1['Over Specific'].cumsum()
master_df_DBA['Not Covered (Monthly)']= table1[' Not Covered']
#master_df_DBA['Spec claimant ID']= table1['REL']
#master_df_DBA['Spec Claimant Amount']= table1['AMT OVER SPEC']

master_df_DBA['Group Id']= values_dict['group']

master_df_DBA['Contract Start']= values_dict['contract_start']
master_df_DBA['Contract End']= values_dict['contract_end']
master_df_DBA['Contract Start']= values_dict['plan_start_date']
#master_df_DBA['Min Attachment Point']= values_dict['min_attachment_point']
#master_df_DBA['Spec Level']= values_dict['spec_level']
master_df_DBA['Agg Factors EE']= values_dict['single']
master_df_DBA['Agg Factors ES']= values_dict['emp+wife']
master_df_DBA['Agg Factors EC']= values_dict['emp_child']
master_df_DBA['Agg Factors Fam']= values_dict['family']
master_df_DBA['Incurred'] = values_dict['incurred']

master_df_DBA['Paid'] = values_dict['paid']


# In[47]:


# Function to remove dollar signs and convert to float
def convert_to_float(value):
    # Check if the value is a string and contains a dollar sign
    if isinstance(value, str) and '$' in value:
        # Remove the dollar sign and commas, then convert to float
        return value.replace('$', '').replace(',', '')
    return value

# Apply the conversion to all elements in the DataFrame
master_df_DBA = master_df_DBA.applymap(convert_to_float)


# In[49]:


master_df_DBA.to_csv(r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\master_df\master_df_DBA.csv")


# In[ ]:




