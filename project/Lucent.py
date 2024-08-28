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
    # Regular expression to extract the incurred and paid values from the 'Contract' string
    pattern = re.compile(r"(\d+)/(\d+)")
    match = pattern.search(contract_str)
    
    if match:
        incurred, paid = match.groups()
        return int(incurred), int(paid)  # Return as integers
    
    return None, None

pdf_path = r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\pdf\Lucent\I02 Group Name_Agg Report.pdf"
labels = ["Min Attachment Pt:", "Plan Year:", "Single:", "Spouse:", "Child:", "Family:", "AggTerm:"]

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
plan_start_date = parse_effective_date(effective_date_str)

contract_str = specific_values.get("AggTerm:", "")
print(contract_str)
incurred, paid = parse_contract_values(contract_str)

incurred_paid_string = text_lines[197]
incurred, paid = incurred_paid_string.split('/')

# Store specific extracted values in a dictionary
values_dict = {
    "group": specific_values.get("GROUP", "Not Found"),
    "spec_level": specific_values.get("Specific:", "Not Found"),
    "Plan Year": specific_values.get("Plan Year:", "Not Found"),
    
    "plan_start_date": plan_start_date,
    "incurred": incurred,
    "paid": paid,
    "min_attachment_point": specific_values.get("Min Attachment Pt:", "Not Found"),
    "single": specific_values.get("Single:", "Not Found"),
    "emp+wife": specific_values.get("Spouse:", "Not Found"),
    "emp_child": specific_values.get("Family:", "Not Found"),
    "family": specific_values.get("Child:", "Not Found"),
}

# Assuming there's a date column to split like before
date_value = values_dict.get("Plan Year")
if date_value and "to" in date_value:
    date_parts = date_value.split('to')
    if len(date_parts) == 2:
        values_dict['contract_start'] = date_parts[0].strip()
        values_dict['contract_end'] = date_parts[1].strip()
    else:
        print("Unexpected date format in the 'From' value")

# Display the dictionary with extracted values
print("Extracted Specific Values in Dictionary Form:")
print(values_dict)


main_table = dataframes['table_1']
main_table

new_headers = main_table.iloc[4]
main_table = main_table.iloc[5:17,:]
main_table.columns = new_headers

main_table

import pandas as pd

# Sample data similar to your mixed DataFrame


df = pd.DataFrame(main_table)

# Split the first mixed column into separate columns
df[['Month', 'Single', 'Family', 'Spouse', 'Child', 'Limited']] = df['Month Single Family Spouse Child Limited'].str.split(expand=True)

# Split the last mixed column into separate columns
#df[['Reimbursed', 'Aggregate', 'Loss Ratio']] = df['Reimbursed Aggregate Loss Ratio'].str.split(expand=True)
df[['Reimbursed', 'Aggregate', 'Loss Ratio']] = df['Reimbursed Aggregate Loss Ratio'].str.split(expand=True)

# Remove the original mixed columns
df.drop(columns=['Month Single Family Spouse Child Limited', 'Reimbursed Aggregate Loss Ratio'], inplace=True)

print(df)


main_table = df

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
master_df_Lucent = pd.DataFrame(columns=columns)

# Print the DataFrame to verify
print("DataFrame with specified columns:")
print(master_df_Lucent)


main_table.columns

master_df_Lucent['Month']= main_table['Month']
master_df_Lucent['Enrollment - EE']= main_table["Single"]
master_df_Lucent['Enrollment - ES']= main_table["Family"]
master_df_Lucent['Enrollment - EC']= main_table["Spouse"]
master_df_Lucent['Enrollment - Fam']= main_table['Child']
master_df_Lucent['Monthly Attachment']= main_table['Accumulation']

#master_df_Lucent['Cumlative Attachment']= main_table['Attachment Point']

master_df_Lucent['Monthly Medical']= main_table['Medical Claims']

master_df_Lucent['Monthly RX']= main_table['Claims']

master_df_Lucent['Monthly Total']= main_table['Paid Claims']
#master_df_Lucent['Total Medical']= table['Total Medical']

#master_df_Lucent['Total RX']= table['Total RX']

#master_df_Lucent['Total Paid']= main_table['YTD Paid Subject To Loss Fund']

#master_df_Lucent['Total Attchment (Running)']= main_table['Attachment Point']

#master_df_Lucent['Total Claims (Running)']= main_table['YTD Paid Subject To Loss Fund']

master_df_Lucent['Spec Claim Amount']= main_table['Reimbursed']
master_df_Lucent['Not Covered (Monthly)']= main_table['Not Covered']

#master_df_Lucent['Group Id']= values_dict['group']

master_df_Lucent['Contract Start']= values_dict['contract_start']
master_df_Lucent['Contract End']= values_dict['contract_end']
master_df_Lucent['Contract Start']= values_dict['plan_start_date']
master_df_Lucent['Min Attachment Point']= values_dict['min_attachment_point']
master_df_Lucent['Spec Level']= values_dict['spec_level']
master_df_Lucent['Agg Factors EE']= values_dict['single']
master_df_Lucent['Agg Factors ES']= values_dict['emp+wife']
master_df_Lucent['Agg Factors EC']= values_dict['emp_child']
master_df_Lucent['Agg Factors Fam']= values_dict['family']



# Function to remove dollar signs and convert to float
def convert_to_float(value):
    # Check if the value is a string and contains a dollar sign
    if isinstance(value, str) and '$' in value:
        # Remove the dollar sign and commas, then convert to float
        return float(value.replace('$', '').replace(',', ''))
    return value

# Apply the conversion to all elements in the DataFrame
master_df_Lucent = master_df_Lucent.applymap(convert_to_float)

master_df_Lucent.to_csv(r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\master_Df_pf\master_df_Lucent.csv")






