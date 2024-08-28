#!/usr/bin/env python
# coding: utf-8

# In[55]:


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
master_df_CBC = pd.DataFrame(columns=columns)

# Print the DataFrame to verify
print("DataFrame with specified columns:")
print(master_df_CBC)


# In[56]:


import pandas as pd

# Ensure the path is correct and use raw string notation for Windows path
file_path = r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\Capital blue cross\STOPLOSS_MTHLY_202406_Group Name_00525834_SLID7836_202306 (2).csv"

try:
    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path, header=None)  # Load without headers to handle custom header row

    # Create a list of column labels 'A' to 'Z'
    column_labels = [chr(i) for i in range(ord('A'), ord('Z') + 1)]

    # Assign these labels to the DataFrame columns
    df.columns = column_labels[:len(df.columns)]
    print(df)

    # Select specific rows if needed, for example from index 0 to 2 (first three rows)
    df = df.iloc[0:50]  # Adjust range as needed

    # Select specific columns from 'A' to 'O' (0 to 18 index-based)
    table = df.iloc[:, 0:18]  # Adjust this range based on the columns you need

    # Further select rows from 14 to 25 (15th to 26th rows, zero-based index)
    table = table.iloc[16:28]

    # Set the 15th row as the header
    new_header = df.iloc[15]
    table.columns = new_header

    # Print the DataFrame to verify it's loaded and modified correctly
    print("DataFrame:")
    print(table)

    # Extract specific values to a dictionary, similar to cell extraction in Excel
    values_dict = {
        # 'min_attachment_point': df.at[37, 'F'],  # Example of accessing a value
        'single': df.at[12, 'B'],
        'emp+wife': df.at[12, 'C'],
        'emp_child': df.at[12, 'D'],
        'family': df.at[12, 'E'],
        # Add more key-value pairs as needed
    }

    # Extract and split contract period dates from the specific row
    date_value = df.at[4, 'A']  # Adjust based on actual data structure
    if pd.notna(date_value):
        # Split the cell content by line breaks
        lines = str(date_value).split('\n')
        for line in lines:
            if "Contract Period Paid Dates:" in line:
                # Split the string by "Through"
                date_parts = line.split('Through')
                if len(date_parts) == 2:
                    contract_start = date_parts[0].replace("Contract Period Paid Dates:", "").strip()
                    contract_end = date_parts[1].strip()

                    # Store the values in the dictionary
                    values_dict['contract_start'] = contract_start
                    values_dict['contract_end'] = contract_end
                    values_dict['plan_start_date'] = contract_start
                else:
                    print("Unexpected format in line for contract dates")
            # Additional processing for other types of lines can be done here

    # Extract values from row 6, column 'A'
    row6_value = df.at[6, 'A']  # Row index 6 corresponds to row 7 in 1-based index
    print("Row 6 Value:", row6_value)  # Debugging: print the entire row value

    # Extract "Aggregating Specific Deductible" value
    if "Aggregating Specific Deductible:" in row6_value:
        # Split the string and get the part after "Aggregating Specific Deductible:"
        spec_level_part = row6_value.split("Aggregating Specific Deductible:")[-1].strip()
        print("Spec Level Part (Raw):", spec_level_part)  # Debugging: print the extracted part
        
        if spec_level_part:
            # Further split based on the next expected field to isolate the number
            spec_level_value = spec_level_part.split("\t\nMinimum Aggregate Attachment Point:")[0].strip()
            print("Spec Level Value (Isolated):", spec_level_value)  # Debugging: print the isolated value
            
            # Remove '$' and ',' then check if the result is a number
            spec_level_value_cleaned = spec_level_value.replace("$", "").replace(",", "")
            print("Spec Level Value (Cleaned):", spec_level_value_cleaned)  # Debugging: print the cleaned value
            
            if spec_level_value_cleaned.replace(".", "").isdigit():
                values_dict['spec_level'] = float(spec_level_value_cleaned)
            else:
                values_dict['spec_level'] = None
    else:
        print("Aggregating Specific Deductible not found in the row.")

    # Extract "Minimum Aggregate Attachment Point" value
    if "Minimum Aggregate Attachment Point:" in row6_value:
        min_attachment_part = row6_value.split("Minimum Aggregate Attachment Point:")[-1].strip()
        if min_attachment_part:
            min_attachment_value = min_attachment_part.replace("$", "").replace(",", "")
            values_dict['min_attachment_point'] = float(min_attachment_value) if min_attachment_value.replace(".", "").isdigit() else None



    row5_value = df.at[5, 'A']
    #print(row5_value)
    if "Contract Type:" in row5_value:
        #contract_type_part = row5_value.split("Contract Type:")[-1].strip()
        print(contract_type_part)
        if contract_type_part:
            incurred_paid = contract_type_part.split('/')
            if len(incurred_paid) == 2:
                incurred_value = incurred_paid[0].strip()
                paid_value = incurred_paid[1].strip()
                values_dict['incurred'] = int(incurred_value) if incurred_value.isdigit() else None
                values_dict['paid'] = int(paid_value) if paid_value.isdigit() else None

    # Print the extracted dictionary
    print("Extracted Values Dictionary:")
    print(values_dict)

except Exception as e:
    print(f"An error occurred: {e}")


# In[57]:


new_column_names = {
    'Total': ['Total_1', 'Total_2', 'Total_3'],
    'Medical': ['Medical_1', 'Medical_2'],
    'RX': ['RX_1', 'RX_2'],
    'Month': ['Month_1', 'Month_2'],
    'YTD': ['YTD_1', 'YTD_2']
}

# Update column names to avoid repetition
current_column_names = table.columns.tolist()
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
table.columns = updated_column_names


# In[58]:


table.columns


# In[59]:


# Function to remove dollar signs and convert to float
def convert_to_float(value):
    # Check if the value is a string and contains a dollar sign
    if isinstance(value, str) and '$' in value:
        # Remove the dollar sign and commas, then convert to float
        return float(value.replace('$', '').replace(',', ''))
    return value

# Apply the conversion to all elements in the DataFrame
table = table.applymap(convert_to_float)


# In[60]:


table


# In[ ]:





# In[61]:


master_df_CBC['Month']= table['Paid\nMonth']
master_df_CBC['Enrollment - EE']= table['Single']
master_df_CBC['Enrollment - ES']= table['Subscriber /\nSpouse']
master_df_CBC['Enrollment - EC']= table['Parent /\nChildren']
master_df_CBC['Enrollment - Fam']= table['Family']
master_df_CBC['Monthly Attachment']= table['Month_2']

master_df_CBC['Cumlative Attachment']= table['YTD_2']

master_df_CBC['Monthly Medical']= table['Medical_2']

master_df_CBC['Monthly RX']= table['RX_2']

master_df_CBC['Monthly Total']= table['Total_3']

master_df_CBC['Total Medical']= table['Medical_2'].cumsum()
master_df_CBC['Total RX']= table['RX_2'].cumsum()
master_df_CBC['Total Paid']= table['Total_3'].cumsum()

master_df_CBC['Total Attchment (Running)']= table['YTD_2']

master_df_CBC['Total Claims (Running)']= table['YTD_1']
master_df_CBC['Spec Claim amount'] = table['Specific\nPayments']
master_df_CBC['Spec Total (running)'] = table['Specific\nPayments'].cumsum()

master_df_CBC['Contract Start']= values_dict['contract_start']
master_df_CBC['Contract End']= values_dict['contract_end']
master_df_CBC['Plan Start Date']= values_dict['plan_start_date']
master_df_CBC['Min Attachment Point']= values_dict['min_attachment_point']
master_df_CBC['Spec Level']= values_dict['spec_level']
master_df_CBC['Agg Factors EE']= values_dict['single']
master_df_CBC['Agg Factors ES']= values_dict['emp+wife']
master_df_CBC['Agg Factors EC']= values_dict['emp_child']
master_df_CBC['Agg Factors Fam']= values_dict['family']
master_df_CBC['Incurred']= values_dict['incurred']
master_df_CBC['Paid']= values_dict['paid']


# In[62]:


master_df_CBC


# In[63]:


master_df_CBC['Spec Total (running)']


# In[64]:


# Function to remove dollar signs and convert to float
def convert_to_float(value):
    # Check if the value is a string and contains a dollar sign
    if isinstance(value, str) and '$' in value:
        # Remove the dollar sign and commas, then convert to float
        return float(value.replace('$', '').replace(',', ''))
    return value

# Apply the conversion to all elements in the DataFrame
master_df_CBC = master_df_CBC.applymap(convert_to_float)


# In[65]:


master_df_CBC.to_csv(r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\\master_df\master_df_CBC.csv")


# In[ ]:




