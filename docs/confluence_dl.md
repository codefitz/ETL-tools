# Confluence PDF Downloader

## Description
This script downloads Confluence pages as PDFs. It starts with a specified page and can go down to nested pages up to a certain depth. It uses a YAML configuration file to read the API token and server information.

## Author
Wes Moskal-Fitzpatrick

## Dependencies
- Python 3.x
- `requests`
- `BeautifulSoup` from `bs4`
- `argparse`
- `re`
- `yaml`
- `os`
- `json`
- `urllib.parse`

## Installation
```bash
pip install requests BeautifulSoup4 PyYAML
```

## Configuration

Create a `config.yaml` file in the same directory as the script. The file should contain:

```yaml
username: YourConfluenceUsername
password: YourConfluencePassword
cf_token: YOUR_CONFLUENCE_API_TOKEN
confluence_server: https://YourConfluenceServer.com
```

Replace the placeholders with your Confluence username, password, and server URL.

## Usage

1. Open terminal and navigate to the directory containing the script.
2. Run the script using the following command:

```bash
python confluence_dl.py <page_url> [--depth DEPTH] [--config CONFIG_PATH] [--save SAVE_LOCATION]
```

- `page_url`: URL of the Confluence page to start downloading from.
- `--depth`: Depth of downloading. Starts with the main page and goes up to 5 levels deep. (default is 1)
- `--config`: Path to the YAML configuration file. (default is `config.yaml`)
- `--save`: Directory to save the downloaded PDFs. (default is current directory)

### Example
```bash
python confluence_dl.py https://your_confluence_server/display/YOUR_PAGE --depth 3 --config config.yaml --save ./pdfs
```

## Warning
When using a high `--depth` number, the script may end up downloading a large number of documents, consuming bandwidth and disk space. Exercise caution and ensure adequate resources are available.

## Troubleshooting
- Make sure you have a valid Confluence API token and server URL in your `config.yaml`.
- If you get an "Unauthorized" error, verify that the API token is correct.
