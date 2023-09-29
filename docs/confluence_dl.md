# Confluence PDF Downloader

## Description

This Python script allows you to download pages from a Confluence site as PDF files. The saved PDFs will be named after the title of the Confluence page.

## Dependencies

- Python 3.x
- `requests`
- `beautifulsoup4`
- `PyYAML`
- `re` (Regular Expression)

## Configuration

Create a `config.yaml` file in the same directory as the script. The file should contain:

```yaml
username: YourConfluenceUsername
password: YourConfluencePassword
confluence_server: https://YourConfluenceServer.com
```

Replace the placeholders with your Confluence username, password, and server URL.

## Usage

1. Open terminal and navigate to the directory containing the script.
2. Run the script using the following command:

   ```
   python script_name.py [page_url] [--depth DEPTH]
   ```

   - `page_url`: The URL of the Confluence page you want to download.
   - `--depth`: Optional. 0 for the main page only, 1 for the main page and directly linked pages. Default is 0.

## Functions

- `sanitize_url(url)`: Sanitizes the given URL.
- `sanitize_filename(filename)`: Sanitizes the filename.
- `read_config(file_path)`: Reads configurations from a YAML file.
- `main(page_url, depth)`: Main function to download the page(s).

---

This README provides an overview of what the script does, its dependencies, configuration, and how to use it. Feel free to adjust as needed.