# ETL Tools

This repository contains various scripts for data extraction and processing. The scripts are designed for internal automation tasks such as downloading content from Confluence, Jira, and Salesforce, creating opportunity folders, validating PDF files, and generating forecasts.

## Configuration

Before running any script, copy the default configuration file and fill in your credentials:

## Installation

Install all Python dependencies with:

```bash
pip install -r requirements.txt
```

# Download Script How 2's:

```bash
cp config_default.yaml config.yaml
```

Edit `config.yaml` and replace the placeholder values (`your_username`, `your_password`, etc.) with your real credentials for Jira, Confluence and Salesforce.

## Available Scripts

| Script | Description |
|-------|-------------|
| `confluence_dl.py` | Download Confluence pages as PDFs. See [docs/confluence_dl.md](docs/confluence_dl.md) for details. |
| `jira_dl.py` | Download Jira tickets as HTML files. See [docs/jira_dl.md](docs/jira_dl.md). |
| `salesforce_dl.py` | Export Salesforce Knowledge articles to `knowledge_articles.json`. See [docs/salesforce_dl.md](docs/salesforce_dl.md). |
| `opp_script.py` | Create opportunity folders from an Excel sheet. See [docs/opp_script.md](docs/opp_script.md). |
| `fitz_validate.py` | Validate PDFs using PyMuPDF and move unreadable files to a `quarantine/` folder. |
| `docx2pdf.py` | Convert `.docx` files to PDF. |
| `xl_refresh.py` | Refresh Dynamics 365 connections in an Excel workbook. |
| `FY-forecast*.py` | Forecast FY data from historical Excel data using Holt-Winters models. |
| `TS-Forecast.py` | Forecast timesheet hours using linear regression. |

## Running a Script

All scripts are standard Python files and can be executed with:

```bash
python <script_name.py> [arguments]
```

Refer to the documentation in the `docs/` directory for script-specific options and examples. For example, to download a Jira ticket you can run:

```bash
python jira_dl.py --issue TICKET-123
```

For more complex workflows, consult the guide corresponding to the script you are using.

