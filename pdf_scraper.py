import requests
from bs4 import BeautifulSoup
import os
import sys
from urllib.parse import urljoin, urlparse
from collections import deque

def is_pdf_link(href):
    return href and href.lower().endswith('.pdf')

def is_internal_link(href, domain):
    parsed = urlparse(href)
    # Relative links or same domain
    return not parsed.netloc or parsed.netloc == domain

def get_pdf_links(page_url):
    try:
        response = requests.get(page_url, timeout=20)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to retrieve {page_url}: {e}")
        return set(), set()

    soup = BeautifulSoup(response.text, "html.parser")
    pdf_links = set()
    page_links = set()
    domain = urlparse(page_url).netloc

    for link in soup.find_all("a", href=True):
        href = link["href"]
        abs_url = urljoin(page_url, href)
        if is_pdf_link(href):
            pdf_links.add(urljoin(page_url, href))
        elif is_internal_link(abs_url, domain):
            # Avoid mailto, javascript, etc.
            if abs_url.startswith("http"):
                page_links.add(abs_url.split("#")[0])  # Remove anchor fragments

    return pdf_links, page_links

def download_pdf(pdf_url, save_dir="."):
    parsed = urlparse(pdf_url)
    filename = os.path.basename(parsed.path)
    if not filename:
        filename = "file.pdf"
    local_path = os.path.join(save_dir, filename)

    if os.path.exists(local_path):
        print(f"Already downloaded: {local_path}")
        return

    print(f"Downloading {pdf_url} -> {local_path}")
    try:
        resp = requests.get(pdf_url, timeout=60)
        resp.raise_for_status()
        with open(local_path, "wb") as f:
            f.write(resp.content)
        print(f"Saved: {local_path}")
    except Exception as e:
        print(f"Failed to download {pdf_url}: {e}")

def scrape_pdfs(start_url, recursive=False):
    visited_pages = set()
    found_pdfs = set()

    queue = deque([start_url])
    while queue:
        url = queue.popleft()
        if url in visited_pages:
            continue
        visited_pages.add(url)
        print(f"Scraping: {url}")
        pdf_links, page_links = get_pdf_links(url)
        for pdf_url in pdf_links:
            if pdf_url not in found_pdfs:
                download_pdf(pdf_url)
                found_pdfs.add(pdf_url)
        if recursive:
            for link in page_links:
                if link not in visited_pages:
                    queue.append(link)

def main():
    if len(sys.argv) < 2:
        print("Usage: python pdf_scraper.py <URL> [--recursive]")
        sys.exit(1)

    url = sys.argv[1]
    recursive = "--recursive" in sys.argv[2:]
    if recursive:
        print("Recursive mode enabled: will follow all internal links.")
    else:
        print("Non-recursive mode: only scraping the provided URL.")

    scrape_pdfs(url, recursive=recursive)

if __name__ == "__main__":
    main()
