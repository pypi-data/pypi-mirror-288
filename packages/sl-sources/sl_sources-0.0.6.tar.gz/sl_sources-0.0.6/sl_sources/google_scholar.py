import asyncio
import hashlib
import io
import json
import re
from typing import Any, Dict, List
from PyPDF2 import PdfReader

from .search import search_google
from .papers import likely_pdf, pubmed_to_pdf_url

from .http import ThrottledClientSession, get_header
from .scrape import browser_scrape, get_browser_and_page

async def search_google_scholar(
    query: str, num_results: int = 10
) -> List[Dict[str, Any]]:
    results = []
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        # set the browser path
        browser, page = await get_browser_and_page(p)

        search_url = f"https://scholar.google.com/scholar?q={query}&num={num_results}"
        try:
            await page.goto(search_url, wait_until="networkidle", timeout=20000)
        except Exception as e:
            # probably timeout and page went ok
            print(f"Error navigating to {search_url}: {str(e)}")
        
        # wait for 3 seconds
        await asyncio.sleep(3)

        for item in await page.query_selector_all(".gs_r.gs_or.gs_scl"):
            title_element = await item.query_selector(".gs_rt a")
            title = await title_element.inner_text() if title_element else ""
            url = await title_element.get_attribute("href") if title_element else ""

            authors_year_element = await item.query_selector(".gs_a")
            authors_year_text = await authors_year_element.inner_text() if authors_year_element else ""
            authors, publication, year = parse_authors_year(authors_year_text)

            snippet_element = await item.query_selector(".gs_rs")
            snippet = await snippet_element.inner_text() if snippet_element else ""
            # set id from hash of the title
            id = hashlib.sha256(title.encode()).hexdigest()

            result = {
                "id": id,
                "title": title,
                "authors": authors,
                "publication": publication,
                "year": year,
                "abstract": snippet,
                "url": url,
                "source_type": "google_scholar",
            }
            results.append(result)

        await browser.close()

        return results[:num_results]

def clean_text(text):
    text = re.sub(r'\u2026', '', text)  # Remove the ellipsis character
    text = re.sub(r'\s*-\s*', '', text)  # Remove any " - "
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    return text.strip()

def parse_authors_year(authors_year_text):
    # Try to extract the year using a regular expression
    year_match = re.search(r'\b(19|20)\d{2}\b', authors_year_text)
    if year_match:
        year = year_match.group()
        authors_publication = authors_year_text.replace(year, '').strip()
    else:
        year = ""
        authors_publication = authors_year_text.strip()
    
    # Split authors and publication
    parts = authors_publication.split("-")
    authors = parts[0].strip()
    publication = "-".join(parts[1:]).strip() if len(parts) > 1 else ""

    # Split authors into an array
    authors_array = [clean_text(author) for author in re.split(r',\s+|\s+and\s+', authors)]
    
    # Clean publication and year
    publication = clean_text(publication)
    year = clean_text(year)

    return authors_array, publication, year


async def download_from_google_scholar(item: Dict[str, Any]) -> Dict[str, Any]:
    async with ThrottledClientSession(rate_limit=15 / 60, headers=get_header()) as session:
        # Check for external identifiers
        if "arxiv" in item["url"]:
            item["url"] = f"https://arxiv.org/pdf/{item['url'].split('/')[-1]}"
        elif "pubmed.ncbi.nlm.nih.gov" in item["url"]:
            item["url"] = await pubmed_to_pdf_url(item["url"], session)
        elif "ncbi.nlm.nih.gov/pmc" in item["url"]:
            pmc_id = item["url"].split("/")[-1]
            item["url"] = f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{pmc_id}/pdf/"
        elif "doi.org" in item["url"]:
            # if item has a doi, use sci-hub to get the pdf
            item["url"] = f"https://sci-hub.wf/{item['url']}"
        try:
            async with session.get(item["url"], allow_redirects=True) as r:
                if r.status == 200 and await likely_pdf(r):
                    content = await r.read()
                    pdf_file = io.BytesIO(content)
                    pdf = PdfReader(pdf_file)
                    full_text = "\n".join(page.extract_text() for page in pdf.pages)
                    if full_text.strip():
                        item["full_text"] = full_text
                        return item
        except Exception as e:
            print(f"Couldn't read PDF: {e}")

            # Try searching for the PDF on Google
            results = await search_google('"' + item["title"] + '"', file_type="pdf", num_results=5)
            if len(results) > 0:
                for result in results:
                    # if result contains books.google, skip
                    if "books.google.com" in result["url"]:
                        continue
                    async with session.get(result["url"], allow_redirects=True) as r:
                        if r.status == 200 and await likely_pdf(r):
                            try:
                                content = await r.read()
                                pdf_file = io.BytesIO(content)
                                pdf = PdfReader(pdf_file)
                                full_text = "\n".join(page.extract_text() for page in pdf.pages)
                                if full_text.strip():
                                    item["full_text"] = full_text
                                    return item
                            except Exception as e:
                                print(f"Couldn't read PDF: {e}")
            else:
                item["full_text"] = await browser_scrape(item["url"])
                return item

        # Scrape the HTML
        try:
            item["full_text"] = await browser_scrape(item["url"])
            return item
        except Exception as e:
            print(f"Couldn't scrape HTML: {e}")

    full_text = "Error downloading or scraping"
    item["full_text"] = full_text
    print ("******** item['url'] is")
    print (item["url"])
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
                for key in ["title", "authors", "year", "url"]
            )

        print("search_google_scholar test passed!")

        # Test the download function asynchronously
        download_tasks = [download_from_google_scholar(result) for result in search_results]
        downloaded_results = await asyncio.gather(*download_tasks)

        # write all of the results to a file
        with open("google_scholar_results.json", "w") as file:
            json.dump(downloaded_results, file)
            
        for downloaded_result in downloaded_results:
            assert (
                len(downloaded_result.get("full_text", "").split()) > 100
            ), "Transcript seems too short"
            print(f"download_from_google_scholar test passed!")

    # start test_main
    asyncio.run(test_main())