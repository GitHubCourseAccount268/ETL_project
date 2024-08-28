import pandas as pd

def create_master_dataframe(columns):
    """
    Create an empty DataFrame with specified columns.
    
    :param columns: List of column names.
    :return: Empty DataFrame with given columns.
    """
    return pd.DataFrame(columns=columns)

def load_and_process_csv(file_path):
    """
    Load and process the CSV file into a DataFrame.
    
    :param file_path: Path to the CSV file.
    :return: Processed DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
        df.columns = [chr(i) for i in range(ord('A'), ord('Z') + 1)][:len(df.columns)]
        df = df.iloc[0:50]  # Adjust range as needed
        table = df.iloc[:, 0:21]
        table = table.iloc[6:18]
        new_header = df.iloc[5]
        table.columns = new_header
        print(table)
        return table
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def convert_columns_to_numeric(table, columns):
    """
    Ensure specified columns are numeric, replacing non-numeric values with NaN.
    
    :param table: DataFrame to process.
    :param columns: List of column names to convert.
    """
    for column in columns:
        table[column] = pd.to_numeric(table[column].str.replace(',', ''), errors='coerce').fillna(0)

def compute_cumulative_sums(table):
    """
    Calculate and add cumulative sum columns to the DataFrame.
    
    :param table: DataFrame to which cumulative sums will be added.
    """
    table['Total Medical'] = table['Medical Claims'].cumsum()
    table['Total RX'] = table['Rx Claims'].cumsum()
    table['Not covered(running)'] = table['Admin Fee'].cumsum()

def update_master_df(master_df, table):
    """
    Update the master DataFrame with values from the processed table.
    
    :param master_df: Master DataFrame to update.
    :param table: Processed table DataFrame.
    """
    master_df['Month'] = table['Month']
    master_df['Enrollment - EE'] = table['EE Only']
    master_df['Enrollment - ES'] = table['EE+ SP']
    master_df['Enrollment - EC'] = table['EE + CH']
    master_df['Enrollment - Fam'] = table['Family']
    master_df['Monthly Medical'] = table['Medical Claims']
    master_df['Monthly RX'] = table['Rx Claims']
    master_df['Total Medical'] = table['Total Medical']
    master_df['Total RX'] = table['Total RX']
    master_df['Not Covered (Monthly)'] = table['Admin Fee']
    master_df['Not Covered (Running)'] = table['Not covered(running)']

def remove_dollar_signs_convert_to_float(df):
    """
    Convert all elements in the DataFrame from dollar sign format to float.
    
    :param df: DataFrame to process.
    """
    def convert_to_float(value):
        if isinstance(value, str) and '$' in value:
            return float(value.replace('$', '').replace(',', ''))
        return value

    return df.applymap(convert_to_float)

# Example usage of the functions:
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

master_df_Humana = create_master_dataframe(columns)

file_path = r"C:\Users\ASUS\Downloads\New folder\Upwork\Data ingestion tool\Humana\ASO_Traditional_Rpt (15).csv"

table = load_and_process_csv(file_path)

if table is not None:
    # Convert specific columns to numeric
    numeric_columns = ['Medical Claims', 'Rx Claims', 'Admin Fee']
    convert_columns_to_numeric(table, numeric_columns)
    
    # Compute cumulative sums
    compute_cumulative_sums(table)
    
    # Update the master DataFrame
    update_master_df(master_df_Humana, table)
    
    # Remove dollar signs and convert to float
    master_df_Humana = remove_dollar_signs_convert_to_float(master_df_Humana)
    
    # Print the final DataFrame to verify
    print("Final Master DataFrame:")
    print(master_df_Humana)

# Function definitions end here.
# You can call these functions in sequence as shown in the example usage section above
