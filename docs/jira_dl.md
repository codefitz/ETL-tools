# Jira Ticket Downloader

## Overview

This Python script allows you to download Jira tickets as HTML files. It provides options to download a specific ticket or all tickets from a specified project. The script uses the Jira API for Python and authenticates using Basic Authentication.

## Requirements

- Python 3.x
- `jira` Python package
- `requests` Python package
- `argparse` Python package
- `PyYAML` Python package

You can install the required packages using pip:

```bash
pip install jira requests argparse PyYAML
```

## Configuration

Before running the script, you must configure the `config.yaml` file in the same directory as your script. The YAML file should contain your Jira username, password, server URL, and project key.

Example `config.yaml`:

```yaml
username: "YOUR_USERNAME"
password: "YOUR_PASSWORD"
jira_server: "https://your.jira.server"
project: "PROJECT_KEY"
```

## Usage

### Download a Specific Issue

To download a specific issue, run the script with the `--issue` flag followed by the issue key:

```bash
python jira_downloader.py --issue ISSUE_KEY
```

Example:

```bash
python jira_downloader.py --issue PROJ-123
```

### Download All Issues from a Project

To download all issues from the project specified in `config.yaml`, simply run the script without the `--issue` flag:

```bash
python jira_downloader.py
```

## Output

The script will save each downloaded ticket as an HTML file in the current working directory. The filename will be the issue key, followed by `.html`.

For example, a ticket with the key `PROJ-123` will be saved as `PROJ-123.html`.

## Note

Please ensure you have the proper permissions to access the Jira server and project specified in `config.yaml`.

## Author

This script was created by Wes Moskal-Fitzpatrick.