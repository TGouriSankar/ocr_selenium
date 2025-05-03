import pandas as pd

# Load the Excel file
input_file = "/media/player/karna1/HYD/andhra-bank-statement_compress/page_2/[0, 1, 2094, 1614]_None.xlsx"  # Replace with your input file path
output_file = "/media/player/karna1/HYD/andhra-bank-statement_compress/page_2/output.xlsx"  # Replace with your desired output file path
import pandas as pd

# Read the Excel file
df = pd.read_excel(input_file)

# Print the original columns for debugging
print(f"Original columns: {df.columns.tolist()}")

# Add empty columns at positions 2 and 5 to match the expected structure
df.insert(2, "Chq No.", "")  # Insert empty "Chq No." column at position 2
df.insert(5, "Credit (Rs.)", "")  # Insert empty "Credit (Rs.)" column at position 5

# Rename columns to match the expected format
df.columns = ["Tran Date", "Transaction Description", "Chq No.", "Debit (Rs.)", "Balance (Rs.)", "Credit (Rs.)"]

# Process the data
# Add a new column for Balance Side from "Debit (Rs.)"
df["Balance Side"] = df["Debit (Rs.)"]

# Save the modified DataFrame to a new Excel file
df.to_excel(output_file, index=False)

print(f"Modified file saved as {output_file}")
