import ssl

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

import asyncio
import hashlib
import io
import json
import traceback
from typing import Any, Dict, List

import aiohttp
from aiohttp import ClientConnectorCertificateError, ClientError
from pyalex import Works
from PyPDF2 import PdfReader

from .papers import likely_pdf

from .http import ThrottledClientSession, get_header
from .scrape import browser_scrape
from .search import search_google

def reconstruct_abstract(inverted_index):
    if not inverted_index:
        return None
    
    words = []
    max_position = max(max(positions) for positions in inverted_index.values())
    
    for i in range(max_position + 1):
        for word, positions in inverted_index.items():
            if i in positions:
                words.append(word)
                break
    
    return ' '.join(words)


async def search_openalex(query: str, num_results: int) -> List[Dict[str, Any]]:
    results = []

    try:
        works = (
            Works()
            .search(query)
            .select(["id", "doi", "title", "publication_year", "authorships", "open_access", "abstract_inverted_index", "ids"])
            .paginate(per_page=num_results)
        )

        for page in works:
            for work in page:
                authors = []
                for authorship in work.get("authorships", []):
                    author = authorship.get("author", {}).get("display_name")
                    if author:
                        authors.append(author)
                authors_str = ", ".join(authors)

                result = {
                    "id": work.get("id"),
                    "doi": work.get("doi"),
                    "authors": authors,
                    "title": work.get("title"),
                    "year": work.get("publication_year"),
                    "url": None,
                    "source_type": "openalex",
                }

                # Resolve URL based on available identifiers
                if work.get("open_access", {}).get("oa_status") == "gold" and work.get("open_access", {}).get("oa_url"):
                    result["url"] = work["open_access"]["oa_url"]
                elif work.get("ids", {}).get("arxiv"):
                    result["url"] = f"https://arxiv.org/pdf/{work['ids']['arxiv']}.pdf"
                elif work.get("ids", {}).get("pmid"):
                    result["url"] = f"https://pubmed.ncbi.nlm.nih.gov/{work['ids']['pmid']}"
                elif work.get("ids", {}).get("pmcid"):
                    result["url"] = f"https://www.ncbi.nlm.nih.gov/pmc/articles/{work['ids']['pmcid']}"

                if result["url"] is None:
                        
                    # Google search for PDF or any other file type
                    try:
                        print(f"attempting google search for pdf: {work['title']} {authors_str}")

                        search_results = await search_google(f'"{work["title"]}" {authors_str}', file_type="pdf", num_results=5)
                        if not search_results or len(search_results) == 0:
                            
                            print(f"no pdf found, searching for html: {work['title']} by {authors_str}")
                            search_results = await search_google(f'"{work["title"]}" {authors_str}', num_results=5)

                        async with ThrottledClientSession(rate_limit=15 / 60, headers=get_header()) as session:
                            print(f"looking for pdf...")
                            for search_result in search_results:
                                try:
                                    async with session.get(search_result["url"], allow_redirects=True) as r:
                                        if r.status == 200 and await likely_pdf(r):
                                            result["url"] = search_result["url"]
                                            break
                                except ClientConnectorCertificateError:
                                    print(f"SSL certificate verification failed for {search_result['url']}")
                                except Exception as e:
                                    print(f"Error checking URL {search_result['url']}: {e}")
                                await asyncio.sleep(1)  # Add a delay between requests

                        if not result["url"] and search_results:
                            result["url"] = search_results[0]["url"]
                    except Exception as e:
                        print(f"Error during Google search for {work['title']}: {e}")

                if result["url"] is None and work.get("doi"):
                    result["url"] = f"https://doi.org/{work['doi']}"

                # Try to get the abstract
                try:
                    abstract_inverted_index = work.get("abstract_inverted_index")
                    if abstract_inverted_index is None:
                        print(f"Debug: No abstract_inverted_index for work {work.get('id')}")
                        # Try to get the abstract directly if available
                        result["abstract"] = work.get("abstract")
                    else:
                        result["abstract"] = reconstruct_abstract(abstract_inverted_index)

                except Exception as e:
                    print(f"Error fetching full work details for {work['id']}: {e}")
                    result["abstract"] = None

                # if the url is still none, lets do a google search for the pdf by name and authors (joined)
                if result["url"] is None:
                    print(f"no url found, searching for any type: {work['title']}")
                    authors_str = ", ".join(authors)
                    search_results = await search_google(f'"{work["title"]}" {authors_str}', file_type="pdf", num_results=5)
                    try:
                        async with ThrottledClientSession(rate_limit=15 / 60, headers=get_header()) as session:
                        # see if its a pdf
                            for search_result in search_results:    
                                async with session.get(search_result["url"], allow_redirects=True) as r:
                                    if r.status == 200 and await likely_pdf(r):
                                        result["url"] = search_result["url"]
                                        break
                                
                            if result["url"] is None and len(search_results) > 0:
                                result["url"] = search_results[0]["url"]
                    except Exception as e:
                        print(f"Error during Google search for {work['title']}: {e}")
                        traceback.print_exc()

                # if the url is still none, lets do a google search, not sorted by pdf
                if result["url"] is None:
                    print(f"no url found, searching for any type: {work['title']}")
                    search_results = await search_google(f'"{work["title"]}" {authors_str}', num_results=5)
                    if search_results:
                        result["url"] = search_results[0]["url"]

                # okay, now we're really in trouble, just search by title, this is extreme edge case
                if result["url"] is None:
                    search_results = await search_google(f'"{work["title"]}"', num_results=5)
                    if search_results and len(search_results) > 0:
                        result["url"] = search_results[0]["url"]

                results.append(result)

            if len(results) >= num_results:
                break

    except Exception as e:
        print(f"Error in search_openalex: {e}")
        traceback.print_exc()

    # Save search results to a JSON file
    try:
        with open("openalex_search_results.json", "w") as file:
            json.dump(results, file, indent=4)
    except Exception as e:
        print(f"Error saving search results to JSON: {e}")

    return results[:num_results]

async def download_and_extract_text(url: str, session: aiohttp.ClientSession) -> str:
    async with session.get(url, allow_redirects=True) as response:
        if response.status == 200:
            content_type = response.headers.get("Content-Type", "").lower()
            if "application/pdf" in content_type:
                pdf_content = await response.read()
                pdf_file = io.BytesIO(pdf_content)
                try:
                    pdf_reader = PdfReader(pdf_file)
                    text = "\n".join(page.extract_text() for page in pdf_reader.pages)
                    return text
                except Exception as e:
                    print(f"Error extracting text from PDF: {e}")
            else:
                return await browser_scrape(url)
        else:
            raise Exception(f"Failed to download content from {url}. Status code: {response.status}")


async def download_from_openalex(work: Dict[str, Any]) -> Dict[str, Any]:
    if "id" not in work:
        work["id"] = hashlib.sha256(work["title"].encode()).hexdigest()

    async with ThrottledClientSession(
        rate_limit=15 / 60, headers=get_header()
    ) as session:
        try:
            work["full_text"] = await download_and_extract_text(work["url"], session)
        except Exception as e:
            print(f"Unexpected error downloading full text: {e}")
            traceback.print_exc()

        if not work.get("full_text"):
            # Search for the PDF on Google
            search_results = await search_google(f'"{work["title"]}"', file_type="pdf", num_results=3)
            for search_result in search_results:
                try:
                    text = await download_and_extract_text(search_result["url"], session)
                    if text:
                        work["full_text"] = text
                        print(f"Downloaded full text from Google search: {search_result['url']}")
                        return work
                except Exception as e:
                    print(f"Error downloading PDF from Google search: {e}")
                    print("Trying next...")

            # Scrape the original URL
            try:
                text = await browser_scrape(work["url"])
                if text:
                    work["full_text"] = text
                    print(f"Downloaded full text from original URL: {work['url']}")
                    return work
            except Exception as e:
                print(f"Error scraping full text: {e}")
                print("Trying google...")
                search_results = await search_google(f'"{work["title"]}"', num_results=3)
                url = search_results[0]["url"]
                text = await download_and_extract_text(url, session)
                if text:
                    work["full_text"] = text
                    print(f"Downloaded full text from Google search: {url}")
                    return work

    return work
async def main():
    query = "Artificial Intelligence"
    num_results = 5

    search_results = await search_openalex(query, num_results)
    print(f"Search results: {len(search_results)}")

    download_tasks = [download_from_openalex(result) for result in search_results]
    downloaded_results = await asyncio.gather(*download_tasks)

    # Save downloaded results to a JSON file
    with open("openalex_downloaded_results.json", "w") as file:
        json.dump(downloaded_results, file, indent=4)


if __name__ == "__main__":
    asyncio.run(main())