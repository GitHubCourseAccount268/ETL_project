#!/usr/bin/env python
# coding: utf-8

# In[159]:


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

pdf_path = r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\pdf\IMS\S7160 - Aggregate (7).pdf"
labels = ["Minimum Attachment Point:", "Contract Dates:","Aggregate Contract:","Group Name", "Single:", "Spouse:", "Child:", "Family:", "AggTerm:"]

# Extracting tables
tables = extract_tables_from_pdf(pdf_path)

# Storing tables as separate DataFrames
dataframes = {}
for i, table in enumerate(tables):
    df_name = f'table_{i + 1}'
    dataframes[df_name] = pd.DataFrame(table)

# Extracting text from the PDF
text = extract_text_from_pdf(pdf_path)

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

contract_str = specific_values.get("Aggregate Contract:", "")
print(contract_str)
incurred, paid = parse_contract_values(contract_str)

incurred_paid_string = text_lines[136]
incurred, paid = incurred_paid_string.split('/')

# Store specific extracted values in a dictionary
values_dict = {
    "group": specific_values.get("Group Name", "Not Found"),
    "spec_level": specific_values.get("Specific:", "Not Found"),
    "Plan Year": specific_values.get("Contract Dates:", "Not Found"),
    
    #"plan_start_date": plan_start_date,
    "incurred": incurred,
    "paid": paid,
    "min_attachment_point": specific_values.get("Minimum Attachment Point:", "Not Found"),
    "single": text_lines[17],
    "emp+wife": text_lines[18],
    "emp_child": text_lines[19],
    "family": text_lines[20],
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
values_dict['plan_start_date'] = values_dict['contract_start']
# Display the dictionary with extracted values
print("Extracted Specific Values in Dictionary Form:")
print(values_dict)


# In[160]:


table1 = dataframes['table_1']
table1


# In[161]:


values_dict['Enrollment member- EE']  = table1.iloc[5:13, 2:3]
values_dict['Enrollment member - ES'] = table1.iloc[5:13, 3:4]
values_dict['Enrollment member - EC'] = table1.iloc[5:13, 4:5]
values_dict['Enrollment member- Fam'] = table1.iloc[5:13, 5:6]
values_dict['single']  = table1.iloc[4, 2]
values_dict['emp+wife'] = table1.iloc[4, 3]
values_dict['emp_child'] = table1.iloc[4, 4]
values_dict['family'] = table1.iloc[4, 5]


# In[162]:


values_dict['Enrollment member- Fam']


# In[163]:


new_headers = table1.iloc[15]
table1 = table1.iloc[16:24,:]
table1.columns = new_headers


# In[164]:


table1


# In[165]:


import pandas as pd

# Sample data similar to your mixed DataFrame


df = pd.DataFrame(table1)

# Split the first mixed column into separate columns
df[['Month', 'Year', 'Monthly att. pt', 'Cumm. Att. pt']] = df['Point Point'].str.split(expand=True, n=3)
df[['Medical', 'Dental']] = df['Paid Paid'].str.split(expand=True, n=1)
df[['Over Specific', 'Not Covered', 'Adjusted', 'Net claims paid', 'Accumulate net claims paid' ]] = df['Specific Covered Adjusted Paid Paid'].str.split(expand=True, n=4)
df[['Aggregate', 'Loss ratio']] = df['Agg Loss Ratio'].str.split(expand=True, n=1)

# Split the last mixed column into separate columns
#df[['Reimbursed', 'Aggregate', 'Loss Ratio']] = df['Reimbursed Aggregate Loss Ratio'].str.split(expand=True)
#df[['Aggregate', 'Loss Ratio']] = df['Reimbursed Aggregate Loss Ratio'].str.split(expand=True)

# Remove the original mixed columns
df.drop(columns=['Point Point', 'Paid Paid','Specific Covered Adjusted Paid Paid','Agg Loss Ratio'], inplace=True)

print(df)


# In[166]:


df


# In[167]:


def correct_values(row):
    # Split the value in the 'Cumlative' column if there's a space
    parts = row['Cumm. Att. pt'].split()
    if len(parts) > 1:
        row['Cumm. Att. pt'] = parts[0]  # Take the first part as 'Cumlative'
        row['Medical'] = parts[1]  # Assign the second part to 'Monthly Medical'
    return row

# Apply the function to the DataFrame
df = df.apply(correct_values, axis=1)


# In[168]:


new_column_names = {
    'Paid': ['Vision paid', 'Rx paid', 'other paid', 'total paid']
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


# In[169]:


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
master_df_IMC = pd.DataFrame(columns=columns)

# Print the DataFrame to verify
print("DataFrame with specified columns:")
print(master_df_IMC)


# In[170]:


table1 = df
df


# In[171]:


# Function to remove dollar signs and convert to float
def convert_to_float(value):
    # Check if the value is a string and contains a dollar sign
    if isinstance(value, str) and '$' in value:
        # Remove the dollar sign and commas, then convert to float
        return float(value.replace('$', '').replace(',', ''))
    return value

# Apply the conversion to all elements in the DataFrame
master_df_IMC = master_df_IMC.applymap(convert_to_float)


# In[172]:


table1['Medical'] = pd.to_numeric(table1['Medical'].str.replace(',', ''), errors='coerce').fillna(0)
table1['Dental'] = pd.to_numeric(table1['Dental'].str.replace(',', ''), errors='coerce').fillna(0)
table1['total paid'] = pd.to_numeric(table1['total paid'].str.replace(',', ''), errors='coerce').fillna(0)
table1['Over Specific'] = pd.to_numeric(table1['Over Specific'].str.replace(',', ''), errors='coerce').fillna(0)
table1['Not Covered'] = pd.to_numeric(table1['Not Covered'].str.replace(',', ''), errors='coerce').fillna(0)


# In[173]:


master_df_IMC['Month']= table1['Month']
master_df_IMC['Enrollment - EE']= values_dict["Enrollment member- EE"]
master_df_IMC['Enrollment - ES']= values_dict["Enrollment member - ES"]
master_df_IMC['Enrollment - EC']= values_dict["Enrollment member - EC"]
master_df_IMC['Enrollment - Fam']= values_dict['Enrollment member- Fam']
master_df_IMC['Monthly Attachment']= table1['Monthly att. pt']

master_df_IMC['Cumlative Attachment']= table1['Cumm. Att. pt']

master_df_IMC['Monthly Medical']= table1['Medical']

master_df_IMC['Monthly RX']= table1['Rx paid']

master_df_IMC['Monthly Total']= table1['total paid']
master_df_IMC['Total Medical']= table1['Medical'].cumsum()

master_df_IMC['Total RX']= table1['Rx paid'].cumsum()

master_df_IMC['Total Paid']= table1['total paid'].cumsum()

master_df_IMC['Total Attchment (Running)']= table1['Cumm. Att. pt']

master_df_IMC['Total Claims (Running)']= table1['total paid']

master_df_IMC['Spec Claim Amount']= table1['Over Specific']

master_df_IMC['Not Covered (Monthly)'] = table1['Not Covered']

master_df_IMC['Not Covered (Running)'] = table1['Not Covered'].cumsum()

master_df_IMC['Spec Claim amount'] = table1['Over Specific']
master_df_IMC['Spec Total (running)'] = table1['Over Specific'].cumsum()
#master_df_IMC['Not Covered (Monthly)']= main_table['Not Covered']

master_df_IMC['Group Id']= values_dict['group']

master_df_IMC['Contract Start']= values_dict['contract_start']
master_df_IMC['Contract End']= values_dict['contract_end']
master_df_IMC['Plan Start Date']= values_dict['plan_start_date']
master_df_IMC['Min Attachment Point']= values_dict['min_attachment_point']
master_df_IMC['Spec Level']= values_dict['spec_level']
master_df_IMC['Agg Factors EE']= values_dict['single']
master_df_IMC['Agg Factors ES']= values_dict['emp+wife']
master_df_IMC['Agg Factors EC']= values_dict['emp_child']
master_df_IMC['Agg Factors Fam']= values_dict['family']
master_df_IMC['Incurred'] = values_dict['incurred']
master_df_IMC['Paid'] - values_dict['paid']


# In[ ]:





# In[174]:


master_df_IMC['Contract End']


# In[175]:


# Function to remove dollar signs and convert to float
def convert_to_float(value):
    # Check if the value is a string and contains a dollar sign
    if isinstance(value, str) and '$' in value:
        # Remove the dollar sign and commas, then convert to float
        return float(value.replace('$', '').replace(',', ''))
    return value

# Apply the conversion to all elements in the DataFrame
master_df_IMC = master_df_IMC.applymap(convert_to_float)


# In[176]:


master_df_IMC.to_csv(r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\master_df\master_df_IMC.csv")


# In[ ]:




