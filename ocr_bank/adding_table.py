import os
import pandas as pd
import re

def process_excel_file(file_path):
    """
    Processes an Excel file by performing the specified steps: 
    - Insert an empty column between the 3rd and 4th columns.
    - Create a new column for conditions.
    - Modify and clean columns based on specific conditions.
    
    Parameters:
        file_path (str): The path to the Excel file to be processed.
        
    Returns:
        pd.DataFrame: The processed DataFrame.
    """
    # Read the Excel file without headers, treating all rows as data
    df = pd.read_excel(file_path, header=None)

    # Insert an empty column between the 3rd and 4th columns (index 3 and 4)
    df.insert(4, ' ', None)

    # Insert a new column for the condition (at the end of the DataFrame)
    df['New Column'] = None

    # Loop through the DataFrame rows
    for index, row in df.iterrows():
        # Check if the value in the 2nd column (index 1) is non-NaN
        if pd.notna(row[1]):
            # Prepend the non-NaN value to the value in the 3rd column (index 2) with a space between them
            df.at[index, 2] = str(row[1]) + ' ' + str(row[2])
            # Empty the value in the 2nd column (index 1)
            df.at[index, 1] = None  # Or use np.nan if you prefer

        # Use regex to find decimal numbers in the 3rd column (index 2)
        if pd.notna(row[2]) and isinstance(row[2], str):
            # Find decimal numbers in the 3rd column (index 2)
            match = re.search(r'\d+\.\d+', row[2])  # Match decimal numbers
            if match:
                # Copy the decimal number to the 4th column (index 3)
                df.at[index, 3] = match.group(0)  # Extract the matched decimal number
                
                # Remove only the decimal number from the 3rd column (index 2), keep the text
                df.at[index, 2] = re.sub(r'\d+\.\d+', '', row[2]).strip()

        # Compare the value in the last column with the previous row's value
        if index > 0:  # Ensure there's a previous row to compare with
            previous_balance = df.iloc[index - 1, -2]  # Second-to-last column of the previous row
            current_balance = df.iloc[index, -2]      # Second-to-last column of the current row

            # Ensure the values are strings, clean them, and convert to float
            if pd.notna(previous_balance) and pd.notna(current_balance):
                previous_balance = float(str(previous_balance).replace(',', ''))
                current_balance = float(str(current_balance).replace(',', ''))
                
                # Check if the current balance is greater than the previous balance
                if current_balance > previous_balance:
                    # Move the data from the 4th column to the new column
                    df.at[index, 'New Column'] = df.at[index, 3]
                    
                    # Remove the value from the 4th column (index 3) after moving to New Column
                    df.at[index, 3] = None

    # Remove the 5th column (currently index 4)
    df.drop(df.columns[4], axis=1, inplace=True)

    # Move the 'New Column' to the 5th column (index 4)
    df.insert(4, 'New Column', df.pop('New Column'))

    # Remove column names by setting the column labels to None
    df.columns = [None] * df.shape[1]

    return df


def merge_excel_files(folder_path, output_file_name=None):
    """
    Merges all Excel files in the given folder into a single Excel file, applying processing steps
    to each file except the first one.
    
    Parameters:
        folder_path (str): The path to the folder containing Excel files.
        output_file_name (str): Optional custom name for the output file. Defaults to the folder name.
        
    Returns:
        str: Path to the merged Excel file.
    """
    is_first_file = True
    all_data = []
    
    # Walk through the folder and process each Excel file
    for root, dirs, files in sorted(os.walk(folder_path)):
        for file in files:
            if file.endswith('.xlsx') or file.endswith('.xls'):
                file_path = os.path.join(root, file)
                
                try:
                    # Read the first file without any processing
                    if is_first_file:
                        df = pd.read_excel(file_path, dtype=str, engine='openpyxl')
                        is_first_file = False  # Set the flag to False after processing the first file
                    else:
                        # Process subsequent files
                        df = process_excel_file(file_path)
                    
                    # Adjust column names of subsequent files to match the first file's columns
                    if len(all_data) > 0:
                        df.columns = all_data[0].columns  # Align columns with the first file's columns
                    
                    # Append the DataFrame to the list
                    all_data.append(df)
                    
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

    # Concatenate all the data into a single DataFrame
    merged_data = pd.concat(all_data, ignore_index=True)
    
    # Define the output file name if not provided
    if not output_file_name:
        output_file_name = f"{os.path.basename(folder_path)}.xlsx"
        
    # Construct the output file path
    output_file = os.path.join(folder_path, output_file_name)
    
    try:
        # Save the merged DataFrame to the output file
        merged_data.to_excel(output_file, index=False, engine='openpyxl')
        print(f"Merged Excel file saved at: {output_file}")
        return output_file
    except Exception as e:
        print(f"Error saving merged file: {e}")
        return None


# # Example usage
folder_path = "/media/player/karna1/HYD/andhra-bank-statement_compress"
merge_excel_files(folder_path)



# import os
# import pandas as pd

# def merge_excel_files(folder_path, output_file_name=None):
#     """
#     Merges all Excel files in the given folder into a single Excel file.
    
#     Parameters:
#         folder_path (str): The path to the folder containing Excel files.
#         output_file_name (str): Optional custom name for the output file. Defaults to the folder name.
        
#     Returns:
#         str: Path to the merged Excel file.
#     """
#     is_first_file = True
#     all_data = []
#     for root, dirs, files in sorted(os.walk(folder_path)):
#         for file in files:
#             if file.endswith('.xlsx') or file.endswith('.xls'):
#                 file_path = os.path.join(root, file)
#                 try:
#                     df = pd.read_excel(file_path, engine='openpyxl')
#                     if len(df.columns) > 3:
#                         if not is_first_file:
#                             df.columns = all_data[0].columns  
#                         all_data.append(df)
#                         is_first_file = False
#                 except Exception as e:
#                     print(f"Error reading {file_path}: {e}")

#     merged_data = pd.concat(all_data, ignore_index=True)
#     if not output_file_name:
#         output_file_name = f"{os.path.basename(folder_path)}.xlsx"
#     output_file = os.path.join(folder_path, output_file_name)
#     try:
#         merged_data.to_excel(output_file, index=False, engine='openpyxl')
#         print(f"Merged Excel file saved at: {output_file}")
#         return output_file
#     except Exception as e:
#         print(f"Error saving merged file: {e}")
#         return None

# # Example usage
# folder_path = "/media/player/karna1/HYD/axis-bank-statement-2024_compress"
# merge_excel_files(folder_path)

# import os
# import pandas as pd

# def preprocess_excel_files(folder_path, processed_folder="processed_files"):
#     """
#     Preprocess Excel files in a folder to ensure column consistency.
#     Adjusts combined data in the last column and saves processed files.
    
#     Parameters:
#         folder_path (str): Path to the folder containing the Excel files.
#         processed_folder (str): Folder to save processed files.
        
#     Returns:
#         str: Path to the folder containing preprocessed files.
#     """
#     os.makedirs(processed_folder, exist_ok=True)  # Create folder for processed files
    
#     for root, dirs, files in sorted(os.walk(folder_path)):
#         for file in files:
#             if file.endswith(".xlsx") or file.endswith(".xls"):
#                 file_path = os.path.join(root, file)
#                 try:
#                     df = pd.read_excel(file_path, dtype=str, engine="openpyxl")
                    
#                     # Check for combined data in the last column
#                     last_column = df.columns[-1]
#                     df_expanded = df[last_column].str.extract(r'(?P<Part1>\d+\.\d{2})(?:\s*(?P<Part2>\d+))?')
                    
#                     if not df_expanded.empty:
#                         df[last_column] = df_expanded["Part1"]
#                         df["Extra_Column"] = df_expanded["Part2"]
                    
#                     # Save processed file
#                     processed_file_path = os.path.join(processed_folder, os.path.basename(file_path))
#                     df.to_excel(processed_file_path, index=False, engine="openpyxl")
#                     print(f"Processed and saved: {processed_file_path}")
#                 except Exception as e:
#                     print(f"Error processing {file_path}: {e}")
    
#     return processed_folder

# def merge_excel_files(folder_path, output_file_name=None):
#     """
#     Merges all preprocessed Excel files in the folder into a single Excel file.
    
#     Parameters:
#         folder_path (str): Path to the folder containing preprocessed Excel files.
#         output_file_name (str): Optional custom name for the output file. Defaults to the folder name.
        
#     Returns:
#         str: Path to the merged Excel file.
#     """
#     all_data = []
#     for root, dirs, files in sorted(os.walk(folder_path)):
#         for file in files:
#             if file.endswith(".xlsx") or file.endswith(".xls"):
#                 file_path = os.path.join(root, file)
#                 try:
#                     df = pd.read_excel(file_path, dtype=str, engine="openpyxl")
#                     all_data.append(df)
#                 except Exception as e:
#                     print(f"Error reading {file_path}: {e}")
    
#     if not all_data:
#         print("No valid data to merge.")
#         return None
    
#     merged_data = pd.concat(all_data, ignore_index=True)
    
#     # Set output file name
#     if not output_file_name:
#         folder_name = os.path.basename(folder_path.strip("/")) or "merged_output"
#         output_file_name = f"{folder_name}.xlsx"
    
#     output_file = os.path.join(folder_path, output_file_name)
#     try:
#         merged_data.to_excel(output_file, index=False, engine="openpyxl")
#         print(f"Merged Excel file saved at: {output_file}")
#         return output_file
#     except Exception as e:
#         print(f"Error saving merged file: {e}")
#         return None

# # Main Function to Process and Merge
# def process_and_merge_excel(folder_path):
#     processed_folder = preprocess_excel_files(folder_path)
#     output_file = merge_excel_files(processed_folder)
#     return output_file

# # Example Usage
# folder_path = "/media/player/karna1/HYD/axis-bank-statement-2024_compress"
# process_and_merge_excel(folder_path)



    






# import os
# import pandas as pd

# folder_path = "/media/player/karna1/HYD/4pg"
# is_first_file = True
# all_data = []

# for root, dirs, files in os.walk(folder_path):
#     for file in files:
#         if file.endswith('.xlsx') or file.endswith('.xls'):
#             file_path = os.path.join(root, file)
#             try:
#                 df = pd.read_excel(file_path, engine='openpyxl')
#                 if not is_first_file:
#                     df.columns = all_data[0].columns  
#                 all_data.append(df)
#                 is_first_file = False  
#             except Exception as e:
#                 print(f"Error reading {file_path}: {e}")

# merged_data = pd.concat(all_data, ignore_index=True)
# output_file = os.path.join(folder_path, f"{os.path.basename(folder_path)}.xlsx")
# try:
#     merged_data.to_excel(output_file, index=False, engine='openpyxl')
#     print(f"Merged Excel file saved at: {output_file}")
# except Exception as e:
#     print(f"Error saving merged file: {e}")

