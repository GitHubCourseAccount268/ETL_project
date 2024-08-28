#!/usr/bin/env python
# coding: utf-8

# In[79]:


import fitz  # PyMuPDF
import pandas as pd

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

def extract_tables_from_text(text):
    tables = []
    lines = text.split('\n')
    current_table = []
    max_columns = 0
    
    for line in lines:
        if line.strip() == "":
            if current_table:
                tables.append(current_table)
                current_table = []
        else:
            current_row = line.split()
            max_columns = max(max_columns, len(current_row))
            current_table.append(current_row)
    
    if current_table:
        tables.append(current_table)

    pandas_tables = []
    for table in tables:
        if table:
            header = table[0]
            data = table[1:]
            adjusted_data = [row + [''] * (max_columns - len(row)) for row in data]  # Adjust rows to have uniform columns
            pandas_tables.append(pd.DataFrame(adjusted_data, columns=header + [''] * (max_columns - len(header))))
    
    return pandas_tables

def extract_specific_values(text, labels):
    extracted_data = {}
    for label in labels:
        start_index = text.find(label)
        if start_index != -1:
            start_index += len(label)
            end_index = text.find('\n', start_index)
            extracted_data[label] = text[start_index:end_index].strip()
    return extracted_data

pdf_path = r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\pdf\ABA\Agg Report.ACE.pdf"
labels = ["Agg Factors", "GROUP",'Specific']  # Replace with your specific labels

# Extracting text from the PDF
text = extract_text_from_pdf(pdf_path)
print(text)

# Extracting tables
tables = extract_tables_from_text(text)

# Extracting specific values
specific_values = extract_specific_values(text, labels)

# Display results
print("Extracted Tables:")
for i, table in enumerate(tables):
    print(f"Table {i + 1}:")
    print(table, "\n")

print("Extracted Specific Values:")
for label, value in specific_values.items():
    print(f"{label}: {value}")


# In[82]:


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
    # Regular expression to extract the incurred and paid values from the 'Contract' string
    pattern = re.compile(r"\((\d+)/(\d+)\)")
    match = pattern.search(contract_str)
    if match:
        incurred, paid = match.groups()
        return int(incurred), int(paid)  # Return as integers
    return None, None

pdf_path = r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\pdf\ABA\Agg Report.ACE.pdf"
labels = ["Agg Factors","GROUP" ,"Specific:",  "Effective", "Contract", "From"]

# Extracting tables
tables = extract_tables_from_pdf(pdf_path)

# Storing tables as separate DataFrames
dataframes = {}
for i, table in enumerate(tables):
    df_name = f'table_{i + 1}'
    dataframes[df_name] = pd.DataFrame(table)

# Extracting text from the PDF
text = extract_text_from_pdf(pdf_path)
print(text)

# Extracting specific values
specific_values = extract_specific_values(text, labels)

# Parse the 'Agg Factors' and 'Effective' fields
agg_factors = specific_values.get("Agg Factors", "")
parsed_factors = parse_agg_factors(agg_factors)
specific_values.update(parsed_factors)

# Extract and parse dates and contract values
effective_date_str = specific_values.get("Effective", "")
plan_start_date = parse_effective_date(effective_date_str)

contract_str = specific_values.get("Contract", "")
incurred, paid = parse_contract_values(contract_str)

# Store specific extracted values in a dictionary
values_dict = {
    "group": specific_values.get("GROUP", "Not Found"),
    "spec_level": specific_values.get("Specific:", "Not Found"),
    "plan_start_date": plan_start_date,
    "incurred": incurred,
    "paid": paid,
    "From": specific_values.get("From", "Not Found"),
    "single": specific_values.get("EMPLOYEE", "Not Found"),
    "emp+wife": specific_values.get("EE+SPOUSE", "Not Found"),
    "emp_child": specific_values.get("FAMILY", "Not Found"),
    "family": specific_values.get("EE+CHILDREN", "Not Found"),
}

# Assuming there's a date column to split like before
date_value = values_dict.get("From")
if date_value and "To" in date_value:
    date_parts = date_value.split('To')
    if len(date_parts) == 2:
        values_dict['contract_start'] = date_parts[0].strip()
        values_dict['contract_end'] = date_parts[1].strip()
    else:
        print("Unexpected date format in the 'From' value")

# Display the dictionary with extracted values
print("Extracted Specific Values in Dictionary Form:")
print(values_dict)


# In[83]:


main_table = dataframes["table_3"]
main_table


# In[84]:


new_headers = main_table.iloc[0] + " " + main_table.iloc[1]
    # Update the DataFrame with new headers
main_table.columns = new_headers
    # Drop the first two rows as they are now headers
main_table = main_table[2:].reset_index(drop=True)


# In[85]:


main_table


# In[86]:


new_column_names = {
    'Subject To Loss Fund': ['Claims Paid Subject To Loss Fund', 'YTD Paid Subject To Loss Fund']
}

# Update column names to avoid repetition
current_column_names = main_table.columns.tolist()
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
main_table.columns = updated_column_names


# In[87]:


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
master_df_ACE = pd.DataFrame(columns=columns)

# Print the DataFrame to verify
print("DataFrame with specified columns:")
print(master_df_ACE)


# In[88]:


tab_2 = dataframes["table_2"]
tab_1 = dataframes["table_1"]


# In[89]:


df_combined = pd.concat([tab_1, tab_2], ignore_index=True)


# In[90]:


rows_to_extract = [0, 3, 6, 9, 12,15,18,21]
extracted_rows = df_combined.iloc[rows_to_extract]


# In[91]:


extracted_rows


# In[92]:


cleaned_data = extracted_rows.dropna(axis=1)


# In[ ]:





# In[93]:


cleaned_data


# In[94]:


main_table.columns


# In[95]:


master_df_ACE['Month']= main_table['Month / Year']
master_df_ACE['Enrollment - EE']= cleaned_data["$20,250.59"]
master_df_ACE['Enrollment - ES']= cleaned_data["$0.00"]
master_df_ACE['Enrollment - EC']= cleaned_data["Unnamed: 2"]
master_df_ACE['Enrollment - Fam']= cleaned_data['Unnamed: 4']
master_df_ACE['Monthly Attachment']= main_table['Monthly Loss Fund']

master_df_ACE['Cumlative Attachment']= main_table['Attachment Point']

#master_df_ACE['Monthly Medical']= table['Medical Claims\nPaid']

#master_df_ACE['Monthly RX']= table['RX Claims Paid']

master_df_ACE['Monthly Total']= main_table['Claims Paid This Month']
#master_df_ACE['Total Medical']= table['Total Medical']

#master_df_ACE['Total RX']= table['Total RX']

master_df_ACE['Total Paid']= main_table['YTD Paid Subject To Loss Fund']

#master_df_ACE['Total Attchment (Running)']= main_table['Attachment Point']

#master_df_ACE['Total Claims (Running)']= main_table['YTD Paid Subject To Loss Fund']

#master_df_ACE['Spec Claim Amount']= main_table['Reimburse Paid YTD']
master_df_ACE['Spec Total (running)']= main_table['Reimburse Paid YTD']


master_df_ACE['Group Id']= values_dict['group']

master_df_ACE['Incurred']= values_dict['incurred']
master_df_ACE['Paid']= values_dict['paid']
master_df_ACE['Contract Start']= values_dict['contract_start']
master_df_ACE['Contract End']= values_dict['contract_end']
master_df_ACE['Plan Start Date']= values_dict['plan_start_date']
#master_df_ACE['Min Attachment Point']= values_dict['min_attachment_point']
master_df_ACE['Spec Level']= values_dict['spec_level']
master_df_ACE['Agg Factors EE']= values_dict['single']
master_df_ACE['Agg Factors ES']= values_dict['emp+wife']
master_df_ACE['Agg Factors EC']= values_dict['emp_child']
master_df_ACE['Agg Factors Fam']= values_dict['family']


# In[ ]:





# In[96]:


master_df_ACE['Contract End']


# In[97]:


# Function to remove dollar signs and convert to float
def convert_to_float(value):
    # Check if the value is a string and contains a dollar sign
    if isinstance(value, str) and '$' in value:
        # Remove the dollar sign and commas, then convert to float
        return float(value.replace('$', '').replace(',', ''))
    return value

# Apply the conversion to all elements in the DataFrame
master_df_ACE = master_df_ACE.applymap(convert_to_float)


# In[98]:


master_df_ACE['Monthly Total']


# In[99]:


master_df_ACE.to_csv(r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\master_df\master_df_ACE.csv")


# In[ ]:




