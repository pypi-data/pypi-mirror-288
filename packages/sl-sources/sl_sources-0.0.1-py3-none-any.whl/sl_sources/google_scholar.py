import mimetypes
import os
import tempfile
from typing import Any, Dict, List
from urllib.parse import urlparse

import requests
from PyPDF2 import PdfReader

from .search import scrape, check_for_playwright


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


async def download_from_google_scholar(
    item: Dict[str, Any]
):
    file_url = item["url"]
    parsed_url = urlparse(file_url)

    if not (parsed_url.scheme and parsed_url.netloc):
        print(f"Invalid URL: {file_url}")
        return ""

    file_extension = os.path.splitext(file_url)[1]
    file_name = f"{item['cid_code']}{file_extension}"

    # with tempfile
    with tempfile.TemporaryDirectory() as output_dir:
        file_path = os.path.join(output_dir, file_name)

        response = requests.get(file_url)

        if response.status_code == 200:
            content_type = response.headers.get("Content-Type", "").lower()

            if "pdf" in content_type:
                file_extension = ".pdf"
            elif "html" in content_type:
                file_extension = ".html"
            else:
                file_extension = mimetypes.guess_extension(content_type) or ".txt"

            with open(file_path, "wb") as file:
                file.write(response.content)
            print(f"Downloaded: {file_name}")

            if file_extension == ".pdf":
                try:
                    with open(file_path, "rb") as file:
                        pdf = PdfReader(file)
                        if len(pdf.pages) == 0:
                            print(f"Error: Empty PDF - {file_name}")
                except:
                    print(f"Error: Invalid PDF - {file_name}")

            return file_path
        else:
            print(f"Failed to download: {file_url}, scraping with browser instead")
            full_text = await scrape(file_url)
            item["full_text"] = full_text
            return item


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
