import pandas as pd

# Define the categorize_transaction function
def categorize_transaction(description):
    description = str(description).lower() 
    if "neft" in description:
        return "NEFT"
    elif "upi" in description:
        return "UPI"
    elif "rtgs" in description:
        return "RTGS"
    elif "imps" in description:
        return "IMPS"
    elif any(word in description for word in ["forex", "foreign", "currency"]):
        return "Foreign Currency Transfer"
    else:
        return "Other"

# List of possible column names
possible_columns = ["Particulars", "Description", "Transaction Description", "Narration"]

# Read the Excel file
file_path = '/media/player/karna1/HYD/andhra-bank-statement_compress/page_1/[36, 836, 2124, 3115]_0.xlsx'  
df = pd.read_excel(file_path)

# Find the correct column for transaction descriptions
description_column = None
for col in possible_columns:
    if col in df.columns:
        description_column = col
        break

# Check if a valid column was found
if description_column is None:
    raise ValueError("None of the expected columns ('Particulars', 'Description', 'Transaction Description') were found in the file.")

# Apply the function to the identified description column and create a new column 'Category'
df['Category'] = df[description_column].apply(categorize_transaction)

# Save the modified DataFrame to a new Excel file
output_file_path = 'categorized_transactions1.xlsx'  
df.to_excel(output_file_path, index=False)

print(f"Categorized transactions saved to {output_file_path}")
