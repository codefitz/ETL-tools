# Author: Wes Moskal-Fitzpatrick
#
# Download from Confluence as PDFs
#

import requests
import json
import argparse
import re
import yaml
import os
from bs4 import BeautifulSoup
from urllib.parse import urlsplit

def read_config(file_path):
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

def sanitize_url(url):
    return url.strip().replace("\n", "").replace("\t", "")

def sanitize_filename(filename):
    return re.sub(r'[\/:*?"<>|]', '', filename)

def get_page_id_from_api(session, page_url):
    page_title = page_url.split('/')[-1]
    api_url = f"{BASE_URL}/rest/api/content?title={page_title}"
    response = session.get(api_url)
    if response.ok:
        data = json.loads(response.text)
        if 'results' in data and len(data['results']) > 0:
            return data['results'][0]['id']
    return None

def download_page_as_pdf(session, page_url, save_location, visited_pages):
    if page_url in visited_pages:
        print(f"Page {page_url} already downloaded. Skipping...")
        return []

    if page_url.startswith("/"):
        full_url = BASE_URL + page_url
    else:
        full_url = page_url
    parsed_url = urlsplit(full_url)
    if 'confluence' not in parsed_url.netloc:
        print(f"Skipping external link: {full_url}")
        return []

    response = session.get(full_url)

    soup = BeautifulSoup(response.content, 'html.parser')

    match = re.search(r'pageId=(\d+)', page_url)
    if match:
        page_id = match.group(1)
    else:
        page_id = get_page_id_from_api(session, page_url)

    if not page_id:
        print(f"Couldn't determine pageId for {page_url}. Skipping...")
        return []

    page_title = sanitize_filename(soup.title.string)
    pdf_export_url = f"{BASE_URL}/spaces/flyingpdf/pdfpageexport.action?pageId={page_id}"
    pdf_response = session.get(pdf_export_url, stream=True)

    filename = os.path.join(save_location, f"{page_title}.pdf")
    with open(filename, 'wb') as f:
        for chunk in pdf_response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    print(f"Downloaded {page_url} as {filename}")
    visited_pages.add(page_url)

    return [a['href'] for a in soup.find_all('a', href=True) if 'viewpage.action?pageId=' in a['href'] or '/display/' in a['href']]

def main(page_url, depth, config_path, save_location):
    config = read_config(config_path)
    TOKEN = config['cf_token']
    global BASE_URL
    BASE_URL = config['confluence_server']

    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {TOKEN}"})

    visited_pages = set()
    queue = [(page_url, 0)]

    while queue:
        url, current_depth = queue.pop(0)
        if current_depth > depth:
            continue
        new_links = download_page_as_pdf(session, url, save_location, visited_pages)
        queue.extend((link, current_depth + 1) for link in new_links)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download Confluence pages as PDFs based on depth.")
    parser.add_argument("page_url", help="The page URL")
    parser.add_argument("--depth", type=int, default=1, choices=[1, 2, 3, 4, 5], help="Depth of downloading: 1 for main page, up to 5 for nested pages.")
    parser.add_argument("--config", default="config.yaml", help="Path to the configuration file.")
    parser.add_argument("--save", default="./", help="Location to save PDF files.")
    args = parser.parse_args()

    main(args.page_url, args.depth, args.config, args.save)
