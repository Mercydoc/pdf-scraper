# PDF Scraper

A simple Python script to scrape and download all PDF files linked on a given web page, with optional recursive subpage scraping.

## Features

- Finds and downloads all PDF links from a given URL.
- Optionally follows all internal links in the website (recursive mode).
- Saves PDFs to the current directory.
- Minimal dependencies.

## Usage

1. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2. Run the scraper for a single page:

    ```bash
    python pdf_scraper.py https://example.com/page-with-pdfs
    ```

3. Run the scraper recursively (all internal pages):

    ```bash
    python pdf_scraper.py https://example.com/page-with-pdfs --recursive
    ```

    This will download **all PDF files linked on the provided page and all subpages of the same site**.

4. All found PDFs will be downloaded to the current directory.

## Options

- By default, only the specified page is scraped.
- Add `--recursive` to follow and scrape all internal links.

## Notes

- This script downloads only PDFs directly linked on the provided web page(s).
- For more complex scraping (pagination, dynamic sites), consider extending with Selenium or Playwright.

## License

MIT
