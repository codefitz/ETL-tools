# Opp_Script

### How to Use the Script

1. **Save the script** as `opp_script.py` or any name you prefer.

2. **Install required packages** if you haven't already:

   ```bash
   pip install pandas openpyxl
   ```

   - `pandas` is used for reading Excel files.
   - `openpyxl` is required by pandas to read `.xlsx` files.

3. **Run the script** from the command line:

   ```bash
   python opp_script.py --excel_file your_excel_file.xlsx --root_dir /path/to/root_directory
   ```

   - Replace `your_excel_file.xlsx` with the path to your Excel file.
   - Replace `/path/to/root_directory` with your actual root directory path.

4. **Optional arguments**:

   - `--opp_number`: Provide an OPP number to lookup its full directory path.

     ```bash
     python opp_script.py --excel_file your_excel_file.xlsx --root_dir /path/to/root_directory --opp_number OPP-0068787
     ```

   - `--file_to_copy`: Specify a file to copy into the OPP folder.

     ```bash
     python opp_script.py --excel_file your_excel_file.xlsx --root_dir /path/to/root_directory --opp_number OPP-0068787 --file_to_copy /path/to/your_file.txt
     ```

### Script Functionality Explained

- **Reading the Excel File**: The script reads the Excel file without headers (`header=None`) to process the data correctly.

- **Processing Rows**: It loops through each row, checking if column B (`row[1]`) contains an OPP number (starts with `'OPP-'`).

- **Retrieving Relative URLs**: When an OPP number is found, it retrieves the Relative URL from column D (`row[3]`).

- **Searching for Subdirectories**: It searches the specified root directory for a subdirectory matching the Relative URL.

- **Creating OPP Folders**: Inside the found subdirectory, it creates a folder named after the OPP number if it doesn't already exist.

- **CSV Output**: The script generates a `opp_paths.csv` file containing two columns: OPP Number and Full Path.

- **OPP Number Lookup**: If an `--opp_number` is provided, the script outputs its full directory path.

- **File Copying**: If `--file_to_copy` is specified, the script copies the file into the OPP folder. If the file already exists, it prompts you to overwrite, rename, or cancel.

   - **Overwrite**: Replaces the existing file.
   - **Rename**: Prompts for a new filename.
   - **Cancel**: Skips the file copy operation.

### Notes and Considerations

- **Directory Search**: The script uses `os.walk` to search for the subdirectory matching the Relative URL. It stops searching once it finds the first match.

- **Case Sensitivity**: The directory search is case-sensitive. Ensure that the Relative URLs and directory names match exactly.

- **Error Handling**: The script prints messages if:

  - The Relative URL is not found.
  - The OPP number is not found in the Excel file.
  - The file to copy cannot be copied because the Relative URL was not found.

- **CSV File**: The `opp_paths.csv` file is created in the current working directory. You can modify the script to specify a different output location if needed.

- **Dependencies**: Ensure all dependencies (`pandas`, `openpyxl`) are installed to avoid import errors.

### Example Usage

```bash
python opp_script.py --excel_file opportunities.xlsx --root_dir /data/projects --opp_number OPP-0068787 --file_to_copy /documents/proposal.docx
```

This command will:

- Process the `opportunities.xlsx` Excel file.
- Search `/data/projects` for the Relative URLs.
- Create OPP folders as needed.
- Output `opp_paths.csv` with the OPP numbers and paths.
- Lookup and display the path for `OPP-0012345`.
- Copy `/documents/proposal.docx` into the `OPP-0012345` folder, handling duplicates as specified.

### Handling Spaces in Command-Line Arguments

The script will handle spaces in filenames and directory paths.

When you run the script from the command line, you need to enclose any filenames or paths that contain spaces within quotes. This ensures that the command-line interpreter passes the entire string (including spaces) as a single argument to the script.

**Example:**

```bash
python opp_script.py --excel_file "my excel file.xlsx" --root_dir "/path/with spaces/"
```

### How the Script Handles Spaces Internally

- **Path Operations:** The script uses Python's `os.path` and `shutil` modules for path manipulations and file operations. These modules are designed to handle paths with spaces seamlessly.

- **String Handling:** All paths and filenames are treated as strings in Python. As long as the strings are correctly passed to the script, spaces within them do not pose any issues.

- **File and Directory Creation:** When creating directories or copying files, the script uses the full paths provided, regardless of whether they contain spaces.

### Important Considerations

- **Enclose Paths in Quotes:** Always enclose paths and filenames with spaces in double quotes (`"`) or single quotes (`'`) when providing them as command-line arguments.

- **Consistent Naming:** Ensure that the names in your Excel file and the directory structure match exactly, including spaces and case sensitivity, to avoid any lookup issues.

### Example Usage with Spaces

```bash
python opp_script.py --excel_file "opportunities with spaces.xlsx" --root_dir "/data/projects with spaces" --opp_number OPP-0012345 --file_to_copy "/documents/proposal with spaces.docx"
```

In this example:

- The Excel file is named `"opportunities with spaces.xlsx"`.
- The root directory is `"/data/projects with spaces"`.
- The file to copy is `"/documents/proposal with spaces.docx"`.


