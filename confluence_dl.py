# Author Wes Moskal-Fitzpatrick
#
# Download from Confluence as PDFs
#

import requests
from bs4 import BeautifulSoup
import argparse
from urllib.parse import urlsplit
import yaml
import re  # Importing Regular Expression library to sanitize filenames

def sanitize_url(url):
    # Removing newlines, spaces, and tabs
    url = url.strip().replace("\n", "").replace("\t", "")
    
    # Further sanitize the URL by unquoting it, which will convert %20 to spaces, etc.
    from urllib.parse import unquote
    return unquote(url)

def sanitize_filename(filename):
    return re.sub(r'[\/:*?"<>|]', '', filename)

def read_config(file_path):
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

def main(page_url, depth):
    config = read_config("config.yaml")
    USERNAME = config['username']
    PASSWORD = config['password']
    BASE_URL = config['confluence_server']
    LOGIN_URL = BASE_URL + "/dologin.action"
    EXPORT_URL = BASE_URL + "/spaces/flyingpdf/pdfpageexport.action"

    session = requests.Session()

    login_data = {
        'os_username': USERNAME,
        'os_password': PASSWORD
    }
    response = session.post(LOGIN_URL, data=login_data)

    if response.ok:
        print("Logged in successfully!")
    else:
        print("Failed to log in.")
        exit()

    # Check if the URL is relative and make it absolute
    if not page_url.startswith('http'):
        page_url = BASE_URL + page_url
        page_url = sanitize_url(page_url)

    # Split the URL
    parsed_url = urlsplit(page_url)
    netloc = parsed_url.netloc

    # Check if netloc contains spaces or @ sign
    if ' ' in netloc or '@' in netloc:
        print(f"Skipping malformed URL: {page_url}")
        return

    # Navigate to the actual page first
    response = session.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract pageId from the soup, if it exists
    page_id_elements = soup.find_all('meta', {'name': 'ajs-page-id'})
    if page_id_elements:
        page_id = page_id_elements[0]['content']
    else:
        print(f"Couldn't determine pageId for {page_url}. Skipping...")
        return
    
    # Download the current page as PDF
    page_title = sanitize_filename(soup.title.string)  # Getting the page title
    pdf_export_url = EXPORT_URL + "?pageId=" + page_id
    pdf_response = session.get(pdf_export_url, stream=True)

    # Save the PDF
    filename = f"{page_title}.pdf"  # Using the title for filename
    #filename = page_id + '.pdf'
    with open(filename, 'wb') as f:
        for chunk in pdf_response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    print(f"Downloaded {page_url} as {filename}")

    # Return links from this page
    return [a['href'] for a in soup.find_all('a', href=True) if 'viewpage.action?pageId=' in a['href'] or '/display/' in a['href']]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download a Confluence page and its directly linked pages as PDFs based on depth.")
    parser.add_argument("page_url", help="The page URL")
    parser.add_argument("--depth", type=int, default=0, choices=[0, 1], help="Depth of downloading: 0 for only main page, 1 for main page and directly linked pages.")
    args = parser.parse_args()

    main(args.page_url, args.depth)
