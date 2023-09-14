# Author Wes Moskal-Fitzpatrick
#
# Download from Confluence as PDFs
#

import requests
from bs4 import BeautifulSoup
import argparse
from urllib.parse import urlsplit

BASE_URL = "https://confluence_url"
LOGIN_URL = BASE_URL + "/dologin.action"
EXPORT_URL = BASE_URL + "/spaces/flyingpdf/pdfpageexport.action"

# Your Confluence credentials
USERNAME = 'username'
PASSWORD = 'password'

def sanitize_url(url):
    # Removing newlines, spaces, and tabs
    url = url.strip().replace("\n", "").replace("\t", "")
    
    # Further sanitize the URL by unquoting it, which will convert %20 to spaces, etc.
    from urllib.parse import unquote
    return unquote(url)

def download_page_as_pdf(session, page_url):
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
        return []

    # Download the current page as PDF
    pdf_export_url = EXPORT_URL + "?pageId=" + page_id
    pdf_response = session.get(pdf_export_url, stream=True)

    # Save the PDF
    filename = page_id + '.pdf'
    with open(filename, 'wb') as f:
        for chunk in pdf_response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    print(f"Downloaded {page_url} as {filename}")

    # Return links from this page
    return [a['href'] for a in soup.find_all('a', href=True) if 'viewpage.action?pageId=' in a['href'] or '/display/' in a['href']]


def main(page_url, depth):
    # Start a session
    session = requests.Session()

    # Log in
    login_data = {
        'os_username': USERNAME,
        'os_password': PASSWORD
    }
    response = session.post(LOGIN_URL, data=login_data)

    # Check if login was successful
    if response.ok:
        print("Logged in successfully!")
    else:
        print("Failed to log in.")
        exit()

    # Maintain a set of pages we've visited to avoid duplication
    visited_pages = set()

    # Download the main page and get its links
    links_on_main_page = download_page_as_pdf(session, page_url)
    visited_pages.add(page_url)

    # If depth is 1, download directly linked pages
    if depth == 1:
        for link in links_on_main_page:
            if link not in visited_pages:
                download_page_as_pdf(session, link)
                visited_pages.add(link)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download a Confluence page and its directly linked pages as PDFs based on depth.")
    parser.add_argument("page_url", help="The page URL, e.g., https://confluence.congenica.net/pages/viewpage.action?pageId=25303698")
    parser.add_argument("--depth", type=int, default=0, choices=[0, 1], help="Depth of downloading: 0 for only main page, 1 for main page and directly linked pages.")
    args = parser.parse_args()

    main(args.page_url, args.depth)

