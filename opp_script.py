import os
import sys
import pandas as pd
import argparse
import csv
import shutil

def main():
    parser = argparse.ArgumentParser(description='Process OPP numbers and directories.')
    parser.add_argument('--excel_file', help='Path to the Excel file')
    parser.add_argument('--root_dir', required=True, help='Root directory to search subdirectories')
    parser.add_argument('--opp_number', help='OPP number to lookup')
    parser.add_argument('--file_to_copy', help='File to copy into the OPP folder')

    args = parser.parse_args()
    
    # Normalize paths
    root_dir = os.path.normpath(args.root_dir)
    opp_number_input = args.opp_number
    file_to_copy = os.path.normpath(args.file_to_copy) if args.file_to_copy else None

    opp_paths = []

    # Process Excel file if provided
    if args.excel_file:
        excel_file = os.path.normpath(args.excel_file)
        try:
            df = pd.read_excel(excel_file, header=None)
        except Exception as e:
            print(f"Error reading Excel file: {e}")
            sys.exit(1)

        # Process rows where both OPP number and Relative URL are present
        for index, row in df.iterrows():
            opp_number_cell = row[1]  # Column index 1 (OPP Number)
            relative_url_cell = row[5]  # Column index 5 (Relative URL)

            # Check if both OPP number and Relative URL are present in the row
            if isinstance(opp_number_cell, str) and opp_number_cell.startswith('OPP-') \
               and isinstance(relative_url_cell, str) and relative_url_cell.strip():
                opp_number = opp_number_cell.strip()
                relative_url = relative_url_cell.strip()

                print(f"Processing OPP Number: {opp_number}, Relative URL: {relative_url}")

                # Search for the Relative URL directory
                found = False
                for dirpath, dirnames, filenames in os.walk(root_dir):
                    dirnames_normalized = [d.strip() for d in dirnames]
                    if relative_url in dirnames_normalized:
                        idx = dirnames_normalized.index(relative_url)
                        matched_dirname = dirnames[idx]
                        found = True
                        subfolder_path = os.path.join(dirpath, matched_dirname)
                        opp_folder_path = os.path.join(subfolder_path, opp_number)

                        # Create OPP folder if it doesn't exist
                        if not os.path.exists(opp_folder_path):
                            try:
                                os.makedirs(opp_folder_path)
                                print(f"Created directory: {opp_folder_path}")
                            except OSError as e:
                                if e.errno == 36 or e.errno == 206:
                                    # errno 36 is "File name too long" on Unix
                                    # errno 206 is "Filename or extension too long" on Windows
                                    print(f"Error: The path is too long to create directory '{opp_folder_path}'. Skipping.")
                                    opp_paths.append((opp_number, 'Path too long'))
                                else:
                                    print(f"Error creating directory '{opp_folder_path}': {e}")
                                    opp_paths.append((opp_number, f'Error: {e}'))
                        else:
                            print(f"Directory already exists: {opp_folder_path}")
                            opp_paths.append((opp_number, opp_folder_path))

                        break  # Stop after finding the correct Relative URL directory

                if not found:
                    print(f"Relative URL '{relative_url}' not found in '{root_dir}'")
                    opp_paths.append((opp_number, 'Relative URL not found'))

            else:
                # Skip rows where either OPP number or Relative URL is missing
                pass

        # Output CSV file
        csv_filename = 'opp_paths.csv'
        try:
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(['OPP Number', 'Full Path'])
                for opp_number, path in opp_paths:
                    csvwriter.writerow([opp_number, path])
        except Exception as e:
            print(f"Error writing CSV file: {e}")

        print(f"CSV file '{csv_filename}' has been created.")

    # Lookup OPP number if provided
    if opp_number_input:
        opp_found = False
        paths_to_search = []

        if opp_paths:
            # Use paths from Excel processing
            paths_to_search = [path for opp_num, path in opp_paths if opp_num == opp_number_input and path != 'Relative URL not found' and path != 'Path too long']
        else:
            # Search for the OPP number directory under root_dir
            for dirpath, dirnames, filenames in os.walk(root_dir):
                if opp_number_input in dirnames:
                    opp_folder_path = os.path.join(dirpath, opp_number_input)
                    paths_to_search.append(opp_folder_path)
                    # Continue searching for more matches

        if paths_to_search:
            opp_found = True
            print(f"OPP Number: {opp_number_input}")
            print("Full Paths:")
            for opp_folder_path in paths_to_search:
                print(f"- {opp_folder_path}")

            # Copy file if specified
            if file_to_copy:
                for opp_folder_path in paths_to_search:
                    dest_file = os.path.join(opp_folder_path, os.path.basename(file_to_copy))
                    try:
                        if os.path.exists(dest_file):
                            choice = input(f"File '{dest_file}' already exists. Overwrite (o), Rename (r), or Cancel (c)? ")
                            if choice.lower() == 'o':
                                shutil.copy2(file_to_copy, dest_file)
                                print(f"File '{file_to_copy}' overwritten to '{dest_file}'")
                            elif choice.lower() == 'r':
                                new_name = input("Enter new filename: ")
                                dest_file = os.path.join(opp_folder_path, new_name)
                                shutil.copy2(file_to_copy, dest_file)
                                print(f"File '{file_to_copy}' copied to '{dest_file}'")
                            else:
                                print("Operation cancelled.")
                        else:
                            shutil.copy2(file_to_copy, dest_file)
                            print(f"File '{file_to_copy}' copied to '{dest_file}'")
                    except OSError as e:
                        if e.errno == 36 or e.errno == 206:
                            print(f"Error: The path is too long to copy file to '{dest_file}'. Skipping.")
                        else:
                            print(f"Error copying file to '{dest_file}': {e}")
        else:
            print(f"OPP Number '{opp_number_input}' not found under '{root_dir}'.")

if __name__ == '__main__':
    main()
