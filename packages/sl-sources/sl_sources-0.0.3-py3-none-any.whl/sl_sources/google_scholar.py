import mimetypes
import os
import re
import tempfile
from typing import Any, Dict, List
from urllib.parse import urlparse
import chardet
import requests
from PyPDF2 import PdfReader

from .search import check_for_playwright, scrape


async def search_google_scholar(
    query: str, num_results: int = 10
) -> List[Dict[str, Any]]:
    results = []
    browser_path = check_for_playwright()
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        # set the browser path
        browser = await p.chromium.launch(headless=True, executable_path=browser_path)
        page = await browser.new_page()
        search_url = f"https://scholar.google.com/scholar?q={query}&num={num_results}"
        await page.goto(search_url)

        for item in await page.query_selector_all(".gs_r.gs_or.gs_scl"):
            title_element = await item.query_selector(".gs_rt a")
            title = await title_element.inner_text() if title_element else ""
            url = await title_element.get_attribute("href") if title_element else ""

            authors_element = await item.query_selector(".gs_a")
            authors = await authors_element.inner_text() if authors_element else ""

            year_element = await item.query_selector(".gs_a")
            year = (
                (await year_element.inner_text()).split("-")[-1].strip()
                if year_element
                else ""
            )

            snippet_element = await item.query_selector(".gs_rs")
            snippet = await snippet_element.inner_text() if snippet_element else ""

            result = {
                "title": title,
                "authors": authors,
                "year": year,
                "abstract": snippet,
                "url": url,
                "cid_code": "",
                "snippet": snippet,
                "source_type": "google_scholar",
            }
            results.append(result)

        await browser.close()

    return results[:num_results]


async def download_from_google_scholar(item: Dict[str, Any]) -> Dict[str, Any]:
    file_url = item["url"]
    parsed_url = urlparse(file_url)

    if not (parsed_url.scheme and parsed_url.netloc):
        print(f"Invalid URL: {file_url}")
        return {"full_text": "", "error": "Invalid URL", "url": file_url}

    def sanitize_filename(filename):
        return re.sub(r'[^\w\-_\. ]', '_', filename)

    file_name = sanitize_filename(item.get('cid_code') or item['title'])

    with tempfile.TemporaryDirectory() as output_dir:
        file_path = os.path.join(output_dir, file_name)
        
        print(f"Attempting to download: {file_url}")
        print(f"File path: {file_path}")

        try:
            response = requests.get(file_url)
            response.raise_for_status()

            content_type = response.headers.get("Content-Type", "").lower()
            if "pdf" in content_type:
                file_extension = ".pdf"
            elif "html" in content_type:
                file_extension = ".html"
            else:
                file_extension = mimetypes.guess_extension(content_type) or ".txt"

            file_path = f"{file_path}{file_extension}"
            
            with open(file_path, "wb") as file:
                file.write(response.content)
            print(f"Downloaded: {file_name}{file_extension}")

            if file_extension == ".pdf":
                try:
                    with open(file_path, "rb") as file:
                        pdf = PdfReader(file)
                        if len(pdf.pages) == 0:
                            return {"full_text": "", "error": f"Empty PDF - {file_name}", "url": file_url}
                        full_text = "\n".join(page.extract_text() for page in pdf.pages)
                except Exception as e:
                    return {"full_text": "", "error": f"Invalid PDF - {file_name}: {str(e)}", "url": file_url}
            else:
                # Detect the file encoding
                with open(file_path, "rb") as file:
                    raw_data = file.read()
                    detected = chardet.detect(raw_data)
                    encoding = detected['encoding']

                print(f"Detected encoding: {encoding}")

                # Read the file with the detected encoding
                with open(file_path, "r", encoding=encoding, errors='replace') as file:
                    full_text = file.read()

            return {"full_text": full_text, "url": file_url}

        except requests.RequestException as e:
            print(f"Failed to download: {file_url}, scraping with browser instead. Error: {str(e)}")
            full_text = await scrape(file_url)
            return {"full_text": full_text, "url": file_url}

        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return {"full_text": "", "error": str(e), "url": file_url }

if __name__ == "__main__":

    async def test_main():
        # Test the search function
        query = "Artificial Intelligence"
        num_results = 5
        search_results = await search_google_scholar(query, num_results)

        assert len(search_results) == num_results
        for result in search_results:
            assert all(
                key in result
                for key in ["title", "authors", "year", "abstract", "url", "cid_code"]
            )

        print("search_google_scholar test passed!")

        # Test the download function
        if search_results:
            downloaded_path = await download_from_google_scholar(search_results[0])
            print(downloaded_path)
            assert (
                len(downloaded_path.get("full_text", "").split()) > 100
            ), "Transcript seems too short"
            print(f"download_from_google_scholar test passed!")
