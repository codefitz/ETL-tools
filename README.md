# ETL Tools

Initially created this repo with some scripts for bulk download of Confluence, Jira and Salesforce docs, and validate/quarantine some buggy PDFs that didn't work and caused privateGPT to throw an error.

Created this new repo to store the scripts seperately.

## Installation

Install all Python dependencies with:

```bash
pip install -r requirements.txt
```

# Download Script How 2's:

[confluence_dl.py](./docs/confluence_dl.md)

[jira_dl.py](./docs/jira_dl.md)

[salesforce_dl.py](./docs/salesforce_dl.md)
[forecast scripts](./docs/forecast_scripts.md)

# privateGPT - primordial

In order to run PrivateGPT on my M2 mac I needed to uninstall and reinstall pymupdf to the latest version as the version PrivateGPT used contains a bug that was compiled with the wrong architecture.

`pip3 install --upgrade --force-reinstall pymupdf`

To ingest HTML you need to update nltk, the easiest way is this:

`python3 -m nltk.downloader all`
https://github.com/imartinez/privateGPT/issues/345