import yaml
import json
from simple_salesforce import Salesforce

# Load credentials from config.yaml
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

sf_username = config['sf_username']
sf_password = config['sf_password']
sf_security_token = config['sf_security_token']

# Initialize Salesforce API connection
sf = Salesforce(username=sf_username, password=sf_password, security_token=sf_security_token)

# Get all field names from the Knowledge__kav object
description = sf.Knowledge__kav.describe()
field_names = [field['name'] for field in description['fields']]

# Create the query string
query_str = f"SELECT {','.join(field_names)} FROM Knowledge__kav"

# Query Knowledge Articles
articles = sf.query_all(query_str)

# Process articles to remove 'attributes' field
cleaned_articles = []
for article in articles['records']:
    cleaned_article = {key: value for key, value in article.items() if key != 'attributes'}
    cleaned_articles.append(cleaned_article)

# Save articles to a JSON file
with open('knowledge_articles.json', 'w') as f:
    json.dump(cleaned_articles, f, indent=4)
