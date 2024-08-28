#!/usr/bin/env python
# coding: utf-8

# In[769]:


import tabula
import fitz  # PyMuPDF
import pandas as pd
import re

def extract_tables_from_pdf(pdf_path):
    return tabula.read_pdf(pdf_path, pages="all", multiple_tables=True)

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
        print(text)
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
    # Regular expression to extract the incurred and paid values, allowing for optional spaces around the slash
    pattern = re.compile(r"(\d+)\s*/\s*(\d+)")
    match = pattern.search(contract_str)
    
    if match:
        incurred, paid = match.groups()
        return int(incurred), int(paid)
    
    return None, None 

pdf_path = r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\pdf\Allied\A23164-01-2023-3174-AGGC (3).pdf"
labels = ["Minimum Attachment:", "Aggregate Contract","Specific Level:","Plan Year:", "Group Name", "Single:", "Single+Sp:", "Single+Ch:", "Family:"]

# Extracting tables
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
agg_factors = specific_values.get("Agg Factors", "")
parsed_factors = parse_agg_factors(agg_factors)
specific_values.update(parsed_factors)

# Extract and parse dates and contract values
effective_date_str = specific_values.get("Plan Year:", "")
#print(effective_date_str)
plan_start_date = parse_effective_date(effective_date_str)

contract_str = specific_values.get("Aggregate Contract", "")
print(contract_str)
incurred, paid = parse_contract_values(contract_str)


incurred_paid_string = text_lines[683]
incurred, paid = incurred_paid_string.split('/')

laser_amount = [text_lines[2], text_lines[3], text_lines[4], text_lines[5], text_lines[6]]


# Store specific extracted values in a dictionary
values_dict = {
    "group": specific_values.get("Group Name", "Not Found"),
    "spec_level": text_lines[658],
    "Plan Year": specific_values.get("Plan Year:", "Not Found"),
    
    "plan_start_date": plan_start_date,
    "incurred": incurred,
    "paid": paid,
    "min_attachment_point": text_lines[55],
    "single": text_lines[671],
    "emp+wife": text_lines[672],
    "emp_child": text_lines[662],
    "family": text_lines[661],
    "laser_amount": laser_amount
}



# Assuming there's a date column to split like before
date_value = values_dict.get("Plan Year")
if date_value and "-" in date_value:
    date_parts = date_value.split('-')
    if len(date_parts) == 2:
        values_dict['contract_start'] = date_parts[0].strip('/')
        values_dict['contract_end'] = date_parts[1].strip('/')
    else:
        print("Unexpected date format in the 'From' value")
values_dict['plan_start_date'] = values_dict['contract_start']
# Display the dictionary with extracted values
print("Extracted Specific Values in Dictionary Form:")
print(values_dict)


# In[770]:


table1 = dataframes['table_1']


# In[771]:


# Function to remove dollar signs and convert to float
def convert_to_float(value):
    # Check if the value is a string and contains a dollar sign
    if isinstance(value, str) and '$' in value:
        # Remove the dollar sign and commas, then convert to float
        return value.replace('$', '').replace(',', '')
    return value

# Apply the conversion to all elements in the DataFrame
table1 = table1.applymap(convert_to_float)


# In[772]:


table1


# In[773]:


new_headers = table1.iloc[0] + " " + table1.iloc[1] + " "+ table1.iloc[2]
    # Update the DataFrame with new headers
table1.columns = new_headers
    # Drop the first two rows as they are now headers
#table1 = table1[2:].reset_index(drop=True)


# In[774]:


table2 = dataframes['table_3']


# In[775]:


#new_headers = table1.iloc[3]
table1 = table1.iloc[3:15,:]
#table1.columns = new_headers


# In[776]:


new_column_names = ['Month', 'Single', 'Single+SP','Single+Ch', 'Nan', 'Fam', 'Total enrollment','Nan','Net Claims','Cumm. Claims','Attachment point','% of Agg','Nan','Savings (Attachmennt pt)']
table1.columns=new_column_names


# In[777]:


table1


# In[778]:


table2 = dataframes['table_2']


# In[779]:


#new_headers = table1.iloc[3]
table2 = table2.iloc[2:13,:]
#table1.columns = new_headers


# In[780]:


new_column_names = ['Month', 'Nan', 'Gross','Nan', 'Medical', 'Nan', 'Pharamacy','Dental','STD','Over Specific','Agg. Specific','Claimss O/S Contract','Prior Year Specific', 'Net Applied to Aggregate']
table2.columns=new_column_names


# In[781]:


table2


# In[782]:


table3 = dataframes['table_3']
table3


# In[783]:


#new_headers = table1.iloc[3]
table3 = table3.iloc[3:15,:]
#table1.columns = new_headers
table3.columns


# In[784]:


new_column_names = ['Month', 'First Name', 'Last Name','REL % OF SPEC', 'Nan', 'RX PAID CLAIMS CUMULATIVE PAID CLAIMS','AGG SPECIFIC','AMT OVER SPEC']
table3.columns=new_column_names


# In[785]:


table3


# In[786]:


import pandas as pd

# Sample data similar to your mixed DataFrame


df = pd.DataFrame(table3)

# Split the first mixed column into separate columns
df[['REL','% od Spec', 'Med Paid Claims']] = df['REL % OF SPEC'].str.split(expand=True, n=2)
df[['Rx Paid claims', 'Cummulative paid claims']] = df['RX PAID CLAIMS CUMULATIVE PAID CLAIMS'].str.split(expand=True, n=1)
#df[['min. attach. pt', '% of ataachement']] = df['Attachment % of Point (120%) Attachment'].str.split(expand=True, n=1)

# Split the last mixed column into separate columns
#df[['Reimbursed', 'Aggregate', 'Loss Ratio']] = df['Reimbursed Aggregate Loss Ratio'].str.split(expand=True)
#df[['Aggregate', 'Loss Ratio']] = df['Reimbursed Aggregate Loss Ratio'].str.split(expand=True)

# Remove the original mixed columns
df.drop(columns=['REL % OF SPEC', 'RX PAID CLAIMS CUMULATIVE PAID CLAIMS'], inplace=True)

print(df)


# In[787]:


table3=df
table3


# In[ ]:





# In[788]:


# Function to remove dollar signs and convert to float
def convert_to_float(value):
    # Check if the value is a string and contains a dollar sign
    if isinstance(value, str) and '$' in value:
        # Remove the dollar sign and commas, then convert to float
        return value.replace('$', '').replace(',', '')
    return value

# Apply the conversion to all elements in the DataFrame
table2 = table2.applymap(convert_to_float)# Function to remove dollar signs and convert to float
def convert_to_float(value):
    # Check if the value is a string and contains a dollar sign
    if isinstance(value, str) and '$' in value:
        # Remove the dollar sign and commas, then convert to float
        return value.replace('$', '').replace(',', '')
    return value

# Apply the conversion to all elements in the DataFrame
table3 = table3.applymap(convert_to_float)


# In[789]:


table3['AMT OVER SPEC']


# In[790]:


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
master_df_Allied = pd.DataFrame(columns=columns)

# Print the DataFrame to verify
print("DataFrame with specified columns:")
print(master_df_Allied)


# In[791]:


table2['Claimss O/S Contract']


# In[792]:


print(table1.columns)
print(table2.columns)
print(table3.columns)

table1['Attachment point'] = pd.to_numeric(table1['Attachment point'].str.replace(',', '').str.replace(' ', ''), errors='coerce').fillna(0)

table2['Claimss O/S Contract'] = pd.to_numeric(table2['Claimss O/S Contract'].str.replace('-', '').str.replace(' ', ''), errors='coerce').fillna(0)

table2['Medical'] = pd.to_numeric(table2['Medical'].str.replace(',', ''), errors='coerce').fillna(0)
table2['Pharamacy'] = pd.to_numeric(table2['Pharamacy'].str.replace(',', '').str.replace('-', ''), errors='coerce').fillna(0)
table2['Gross'] = pd.to_numeric(table2['Gross'].str.replace(',', '').str.replace(' ', ''),errors='coerce').fillna(0)
table2['Over Specific'] = pd.to_numeric(table2['Over Specific'].str.replace(',', '').str.replace('-', ''),errors='coerce').fillna(0)

table2['Total Medical'] = table2['Medical'].cumsum()

table2['Total Rx'] = table2['Pharamacy'].cumsum()

table2['Total paid'] = table2['Gross'].cumsum()

table2['Total Over Specific'] = table2['Over Specific'].cumsum()

table1['Cumm. Attachment point'] = table1['Attachment point'].cumsum()
table2['Total running monntlhy not covered '] = table2['Claimss O/S Contract'].cumsum()


# In[793]:


table2['Claimss O/S Contract']


# In[794]:


master_df_Allied['Month']= table1['Month']
master_df_Allied['Enrollment - EE']= table1["Single"]
master_df_Allied['Enrollment - ES']= table1["Single+SP"]
master_df_Allied['Enrollment - EC']= table1["Single+Ch"]
master_df_Allied['Enrollment - Fam']= table1['Fam']
master_df_Allied['Monthly Attachment']= table1['Attachment point']

master_df_Allied['Cumlative Attachment']= table1['Cumm. Attachment point']

master_df_Allied['Monthly Medical']= table2['Medical']

master_df_Allied['Monthly RX']= table2['Pharamacy']

master_df_Allied['Monthly Total']= table2['Gross']
master_df_Allied['Total Medical']= table2['Total Medical']

master_df_Allied['Total RX']= table2['Total Rx']

master_df_Allied['Total Paid']= table2['Total paid']

master_df_Allied['Total Attchment (Running)']= table1['Cumm. Attachment point']

master_df_Allied['Total Claims (Running)']= table1['Cumm. Claims']

master_df_Allied['Spec Claim amount']= table2['Over Specific']
master_df_Allied['Not Covered (Monthly)']= table2['Claimss O/S Contract']
master_df_Allied['Not Covered (Running)']= table2['Total running monntlhy not covered ']
master_df_Allied['Spec claimant ID']= table3['REL']
master_df_Allied['Spec Claimant Amount']= table3['AMT OVER SPEC']
master_df_Allied['Spec Total (running)']= table2['Total Over Specific']


master_df_Allied['Group Id']= values_dict['group']
#master_df_Allied['Laser Amount']= values_dict['laser_amount']
master_df_Allied['Contract Start']= values_dict['contract_start']
master_df_Allied['Contract End']= values_dict['contract_end']
master_df_Allied['Plan Start Date']= values_dict['plan_start_date']
master_df_Allied['Incurred']= values_dict['incurred']
master_df_Allied['Paid']= values_dict['paid']
master_df_Allied['Min Attachment Point']= values_dict['min_attachment_point']
master_df_Allied['Spec Level']= values_dict['spec_level']
master_df_Allied['Agg Factors EE']= values_dict['single']
master_df_Allied['Agg Factors ES']= values_dict['emp+wife']
master_df_Allied['Agg Factors EC']= values_dict['emp_child']
master_df_Allied['Agg Factors Fam']= values_dict['family']


# In[ ]:





# In[795]:


master_df_Allied['Contract Start']


# In[796]:


import numpy as np

# Assume values_dict['laser_amount'] is a list with fewer elements than the number of rows in master_df_Allied
laser_amount = values_dict['laser_amount']

# Check the length of master_df_Allied
num_rows = len(master_df_Allied)

# Create a new column with NaN values
master_df_Allied['Laser Amount'] = np.nan

# Assign the available values to the beginning of the column
master_df_Allied.loc[:len(laser_amount) - 1, 'Laser Amount'] = laser_amount

# If you need to fill the rest with a default value (e.g., 0), you can do:
# master_df_Allied['Laser Amount'].fillna(0, inplace=True)

print(master_df_Allied)


# In[ ]:


master_df_Allied['Laser Amount']


# In[ ]:


# Function to remove dollar signs and convert to float
def convert_to_float(value):
    # Check if the value is a string and contains a dollar sign
    if isinstance(value, str) and '$' in value:
        # Remove the dollar sign and commas, then convert to float
        return float(value.replace('$', '').replace(',', ''))
    return value

# Apply the conversion to all elements in the DataFrame
master_df_Allied = master_df_Allied.applymap(convert_to_float)


# In[ ]:





# In[ ]:


master_df_Allied.to_csv(r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\master_df\master_df_Allied.csv")


# In[ ]:




