# Fork of PrivateGPT

Created this fork to store a couple of scripts for bulk download of Confluence, Jira and Salesforce docs, and validate/quarantine some buggy PDFs that didn't work and caused GPT to throw an error.

In order to run PrivateGPT on my M2 mac I needed to uninstall and reinstall pymupdf to the latest version as the version PrivateGPT used contains a bug that was compiled with the wrong architecture.

`pip3 install --upgrade --force-reinstall pymupdf`

To ingest HTML you need to update nltk, the easiest way is this:

`python3 -m nltk.downloader all`
https://github.com/imartinez/privateGPT/issues/345

# Download Script How 2's:

[confluence_dl.py](./docs/confluence_dl.md)

[jira_dl.py](./docs/jira_dl.md)

[salesforce_dl.py](./docs/salesforce_dl.md)