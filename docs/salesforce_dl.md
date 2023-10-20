# Salesforce Knowledge Download

## Description

This Python script fetches articles from a Salesforce `Knowledge__kav` object and saves them as a JSON file. It uses the Salesforce API for querying and is capable of dynamically obtaining all fields of the object.

## Requirements

- Python 3.x
- `simple_salesforce` Python package
- `PyYAML` Python package

## Installation

1. Install the required Python packages:

    ```bash
    pip install simple_salesforce PyYAML
    ```

## Configuration

1. Create a `config.yaml` file in the same directory as the script.

2. Add your Salesforce credentials to `config.yaml`:

    ```yaml
    sf_username: 'your_username'
    sf_password: 'your_password'
    sf_security_token: 'your_security_token'
    ```

## Usage

Run the script:

```bash
python salesforce_dl.py
```

This will create a file called `knowledge_articles.json` containing all articles from the Salesforce `Knowledge__kav` object.