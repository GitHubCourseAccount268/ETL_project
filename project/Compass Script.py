#!/usr/bin/env python
# coding: utf-8

# In[57]:


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
        #print(text)
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

pdf_path = r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\pdf\Compass Health\2022 Agg report[22].pdf"
labels = ["MinimumAttachmentPoint", "SpecDeductible","ContractType","GroupName", "Single", "EE+SP", "EE+CH", "Family"]

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
effective_date_str = specific_values.get("Contract Dates:", "")
#print(effective_date_str)
plan_start_date = parse_effective_date(effective_date_str)

contract_str = specific_values.get("ContractType", "")
print(contract_str)
incurred, paid = parse_contract_values(contract_str)


incurred_paid_string = text_lines[4]
incurred, paid = incurred_paid_string.split('/')

# Store specific extracted values in a dictionary
values_dict = {
      
    "group": specific_values.get("Group Name", "Not Found"),
    "spec_level": text_lines[9],
    "Plan Year": specific_values.get("Plan Year:", "Not Found"),
    
    "plan_start_date": plan_start_date,
    "incurred": incurred,
    "paid": paid,
    "min_attachment_point": text_lines[24],
    "single": text_lines[12],
    "emp+wife": text_lines[15],
    "emp_child": text_lines[18],
    "family": text_lines[21],
}

# Assuming there's a date column to split like before
date_value = values_dict.get("Plan Year")
if date_value and "-" in date_value:
    date_parts = date_value.split('-')
    if len(date_parts) == 2:
        values_dict['contract_start'] = date_parts[0].strip()
        values_dict['contract_end'] = date_parts[1].strip()
    else:
        print("Unexpected date format in the 'From' value")
#values_dict['plan_start_date'] = values_dict['contract_start']
# Display the dictionary with extracted values
print("Extracted Specific Values in Dictionary Form:")
print(values_dict)


# In[58]:


table1=dataframes['table_1']


# In[59]:


# Function to remove dollar signs and convert to float
def convert_to_float(value):
    # Check if the value is a string and contains a dollar sign
    if isinstance(value, str) and '$' in value:
        # Remove the dollar sign and commas, then convert to float
        return value.replace('$', '').replace(',', '')
    return value

# Apply the conversion to all elements in the DataFrame
table1 = table1.applymap(convert_to_float)


# In[60]:


table1


# In[61]:


new_headers = table1.iloc[2] + " " + table1.iloc[3]
    # Update the DataFrame with new headers
table1.columns = new_headers
    # Drop the first two rows as they are now headers
#table1 = table1[2:].reset_index(drop=True)


# In[62]:


#new_headers = table1.iloc[3]
table1 = table1.iloc[4:16,:]
#table1.columns = new_headers


# In[63]:


table1


# In[64]:


new_column_names = {
    'NaN': ['Month', 'EE', 'EE+SP EE+CH', 'Fam', 'Expected Claims', ]
}

# Update column names to avoid repetition
current_column_names = df.columns.tolist()
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
df.columns = updated_column_names


# In[65]:


new_column_names = ['Month', 'EE', 'EE+SP EE+CH', 'Fam', 'Expected Claims', 'blank1','Attachment Medical Claims Prescription Point (120%) Paid Claims Paid','blank2','TOTAL CLAIMS PAID','blank3','Specific (Stop Loss Reimb.)','net paid claims','Cumulative Total Paid Claims','blank4','Attachment % of Point (120%) Attachment']
table1.columns=new_column_names


# In[66]:


table1


# In[67]:


import pandas as pd

# Sample data similar to your mixed DataFrame


df = pd.DataFrame(table1)

# Split the first mixed column into separate columns
df[['EE+SP','EE+CH']] = df['EE+SP EE+CH'].str.split(expand=True, n=1)
df[['Monthly attachement', 'Medical', 'Prescription']] = df['Attachment Medical Claims Prescription Point (120%) Paid Claims Paid'].str.split(expand=True, n=2)
df[['min. attach. pt', '% of ataachement']] = df['Attachment % of Point (120%) Attachment'].str.split(expand=True, n=1)

# Split the last mixed column into separate columns
#df[['Reimbursed', 'Aggregate', 'Loss Ratio']] = df['Reimbursed Aggregate Loss Ratio'].str.split(expand=True)
#df[['Aggregate', 'Loss Ratio']] = df['Reimbursed Aggregate Loss Ratio'].str.split(expand=True)

# Remove the original mixed columns
df.drop(columns=['EE+SP EE+CH', 'Attachment Medical Claims Prescription Point (120%) Paid Claims Paid','Attachment % of Point (120%) Attachment'], inplace=True)

print(df)


# In[68]:


table1 = df


# In[ ]:





# In[69]:


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
master_df_Compass = pd.DataFrame(columns=columns)

# Print the DataFrame to verify
print("DataFrame with specified columns:")
print(master_df_Compass)


# In[70]:


table1.columns


# In[71]:


table1['Specific (Stop Loss Reimb.)']


# In[72]:


table1['Medical'] = pd.to_numeric(table1['Medical'].str.replace(',', ''), errors='coerce').fillna(0)
table1['Prescription'] = pd.to_numeric(table1['Prescription'].str.replace(',', ''), errors='coerce').fillna(0)
table1['TOTAL CLAIMS PAID'] = pd.to_numeric(table1['TOTAL CLAIMS PAID'].str.replace(',', ''), errors='coerce').fillna(0)

table1['Monthly attachement'] = pd.to_numeric(table1['Monthly attachement'].str.replace(',', ''), errors='coerce').fillna(0)
table1['Specific (Stop Loss Reimb.)'] = pd.to_numeric(table1['Specific (Stop Loss Reimb.)'].str.replace(',', ''), errors='coerce').fillna(0)


# Calculate the cumulative sum
#table['YTD paid'] = table['Net Paid'].cumsum()
table1['Total Medical'] = table1['Medical'].cumsum()
table1['Total RX'] = table1['Prescription'].cumsum()
table1['Total Paid'] = table1['TOTAL CLAIMS PAID'].cumsum()
table1['Cummalative attachment'] = table1['Monthly attachement'].cumsum()
table1['Spec claim amount (running)'] = table1['Specific (Stop Loss Reimb.)'].cumsum()



# In[74]:


master_df_Compass['Month']= table1['Month']
master_df_Compass['Enrollment - EE']= table1["EE"]
master_df_Compass['Enrollment - ES']= table1["EE+SP"]
master_df_Compass['Enrollment - EC']= table1["EE+CH"]
master_df_Compass['Enrollment - Fam']= table1['Fam']
master_df_Compass['Monthly Attachment']= table1['Monthly attachement']

#master_df_Compass['Cumlative Attachment']= table1['Cumm. Att. pt']

master_df_Compass['Monthly Medical']= table1['Medical']

master_df_Compass['Monthly RX']= table1['Prescription']

master_df_Compass['Monthly Total']= table1['TOTAL CLAIMS PAID']
master_df_Compass['Total Medical']= table1['Total Medical']

master_df_Compass['Total RX']= table1['Total RX']

master_df_Compass['Total Paid']= table1['Total Paid']

master_df_Compass['Total Attchment (Running)']= table1['min. attach. pt']

master_df_Compass['Total Claims (Running)']= table1['net paid claims']

master_df_Compass['Spec Claim Amount']= table1['Specific (Stop Loss Reimb.)']
master_df_Compass['Spec Total (running)']= table1['Spec claim amount (running)']
#master_df_Compass['Not Covered (Monthly)']= main_table['Not Covered']

master_df_Compass['Group Id']= values_dict['group']

#master_df_Compass['Contract Start']= values_dict['contract_start']
#master_df_Compass['Contract End']= values_dict['contract_end']
#master_df_Compass['Contract Start']= values_dict['plan_start_date']
master_df_Compass['Min Attachment Point']= values_dict['min_attachment_point']
master_df_Compass['Spec Level']= values_dict['spec_level']
master_df_Compass['Agg Factors EE']= values_dict['single']
master_df_Compass['Agg Factors ES']= values_dict['emp+wife']
master_df_Compass['Agg Factors EC']= values_dict['emp_child']
master_df_Compass['Agg Factors Fam']= values_dict['family']
master_df_Compass['Incurred'] = values_dict['incurred']

master_df_Compass['Paid'] = values_dict['paid']


# In[76]:


master_df_Compass['Incurred']


# In[78]:


# Function to remove dollar signs and convert to float
def convert_to_float(value):
    # Check if the value is a string and contains a dollar sign
    if isinstance(value, str) and '$' in value:
        # Remove the dollar sign and commas, then convert to float
        return float(value.replace('$', '').replace(',', ''))
    return value

# Apply the conversion to all elements in the DataFrame
master_df_Compass = master_df_Compass.applymap(convert_to_float)


# In[79]:


master_df_Compass.to_csv(r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\master_Df_pf\master_df_Compass.csv")


# In[ ]:




