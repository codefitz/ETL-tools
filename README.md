# Fork of PrivateGPT

Created this fork to store a couple of scripts for bulk download of Confluence docs, and validate/quarantine some buggy PDFs that didn't work and caused GPT to throw an error.

In order to run PrivateGPT on my M2 mac I needed to uninstall and reinstall pymupdf to the latest version as the version PrivateGPT used contains a bug that was compiled with the wrong architecture.

`pip install --upgrade --force-reinstall pymupdf`