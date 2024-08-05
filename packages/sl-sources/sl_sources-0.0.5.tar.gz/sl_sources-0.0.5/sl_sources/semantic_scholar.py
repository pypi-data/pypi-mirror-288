import asyncio
import hashlib
import io
import json
import os
import re
import traceback

from PyPDF2 import PdfReader

import asyncio

from .search import search_google

from .http import ThrottledClientSession, get_header
from .papers import likely_pdf
from .scrape import browser_scrape


async def search_semantic_scholar(
    query,
    num_results=10,
    semantic_scholar_api_key=None,
    _offset=0,
):
    endpoint = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "fields": ",".join(
            [
                "title",
                "year",
                "authors",
                "citationStyles",
                "externalIds",
                "url",
                "openAccessPdf",
                "isOpenAccess",
                # "influentialCitationCount",
                "tldr",
            ]
        ),
        "limit": num_results,
        "offset": _offset,
    }
    ssheader = get_header()
    if semantic_scholar_api_key is not None:
        ssheader["x-api-key"] = semantic_scholar_api_key
    else:
        ssheader["x-api-key"] = os.environ.get("SEMANTIC_SCHOLAR_API_KEY", "")

    async with ThrottledClientSession(
        rate_limit=15 / 60, headers=ssheader
    ) as ss_session:
        async with ss_session.get(url=endpoint, params=params) as response:
            if response.status != 200:
                raise Exception(
                    f"Error searching papers: {response.status} {response.reason} {await response.text()}"
                )
            data = await response.json()
            papers = data.get("data", [])
            # papers.sort(key=lambda x: x["influentialCitationCount"], reverse=True)

    results = []
    for paper in papers[:num_results]:
        title = paper["title"]
        year = paper["year"]
        authors = [author["name"] for author in paper["authors"]]

        bibtex = paper["citationStyles"]["bibtex"]

        # if there is an ArXiv external ID, resolve this as the URL
        if "arXiv" in paper["externalIds"]:
            paper["url"] = f"https://arxiv.org/pdf/{paper['externalIds']['arXiv']}"

        # if openAccessPdf is a URL, use that
        if (
            "openAccessPdf" in paper
            and paper["openAccessPdf"] is not None
            and "url" in paper["openAccessPdf"]
        ):
            paper["url"] = paper["openAccessPdf"]["url"]

        elif "PubMed" in paper["externalIds"]:
            paper["url"] = (
                f"https://pubmed.ncbi.nlm.nih.gov/{paper['externalIds']['PubMed']}"
            )

        elif "PMC" in paper["externalIds"]:
            paper["url"] = (
                f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{paper['externalIds']['PMC']}"
            )

        elif "DOI" in paper["externalIds"]:
            paper["url"] = f"https://sci-hub.wf/{paper['externalIds']['DOI']}"
        else:
            # try to find the pdf by name?
            pass

        result = {
            "id": paper["paperId"],
            "title": title,
            "abstract": paper["tldr"],
            "year": year,
            "authors": authors,
            "url": paper["url"],
            "source_type": "semantic_scholar",
        }
        results.append(result)

    return results


async def download_from_semantic_scholar(paper):
    if "id" not in paper:
        paper["id"] = hashlib.sha256(paper["url"].encode()).hexdigest()

    async with ThrottledClientSession(
        rate_limit=15 / 60, headers=get_header()
    ) as session:
        async with session.get(paper["url"], allow_redirects=True) as r:
            try:
                if r.status != 200 or not await likely_pdf(r):
                    raise Exception(f"No paper with id {paper['id']}")

                content = await r.read()  # Read the content
                pdf_file = io.BytesIO(content)  # Create BytesIO object
                pdf = PdfReader(pdf_file)  # Pass BytesIO object to PdfReader
                full_text = "\n".join(page.extract_text() for page in pdf.pages)
                if full_text.strip():  # Check if the text is empty or whitespace
                    paper["full_text"] = full_text
                    return paper
            except Exception as e:
                print(f"Couldn't read PDF the easy way: {e}")

        # if we couldnt get the pdf the easy way, lets try another way
        # if the paper has a title, lets try to google search it but focused on pdf
        results = await search_google(
            '"' + paper["title"] + '"', file_type="pdf", num_results=3
        )
        if len(results) > 0:
            print(f"Found {len(results)} results for {paper['title']}")
            for result in results:
                # try to download the pdf
                try:
                    async with session.get(result["url"], allow_redirects=True) as r:
                        if r.status != 200 or not await likely_pdf(r):
                            raise Exception(f"No paper with id {paper['id']}")
                        content = await r.read()
                        pdf_file = io.BytesIO(content)
                        pdf = PdfReader(pdf_file)
                        full_text = "\n".join(page.extract_text() for page in pdf.pages)
                        if full_text.strip():  # Check if the text is empty or whitespace
                            print("Found full text")
                            # print first 100 characters
                            print(full_text[:100])
                            paper["full_text"] = full_text
                            return paper
                except Exception as e:
                    print(f"Couldn't read PDF from google result: {e}")
                    # stack trace
                    traceback.print_exc()

            # if none of the results have a full text, lets scrape it
            text = await browser_scrape(paper["url"])
            paper["full_text"] = text
            return paper


if __name__ == "__main__":
    query = "Artificial Intelligence"
    num_results = 2

    def run_search_papers(query, num_results=10, semantic_scholar_api_key=None):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(
            search_semantic_scholar(query, num_results, semantic_scholar_api_key)
        )

    # Search for papers
    search_results = run_search_papers(query, num_results)
    print(f"Search results: {search_results}")

    def run_download_from_semantic_scholar_sync(papers):
        async def run_download_from_semantic_scholar(papers):
            tasks = [download_from_semantic_scholar(paper) for paper in papers]
            return await asyncio.gather(*tasks)
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(run_download_from_semantic_scholar(papers))

    # Download papers
    downloaded_papers = run_download_from_semantic_scholar_sync(search_results)
    # save all downloaded papers to ./test_results
    with open("./test_results.json", "w") as f:
        json.dump(downloaded_papers, f, indent=4, ensure_ascii=False)
        
    assert len(search_results) == num_results
    for result in search_results:
        assert all(key in result for key in ["id", "authors", "url", "year"])

    for result in downloaded_papers:
        assert all(key in result for key in ["id", "authors", "url", "year", "full_text"])

    print("search_semantic_scholar and download_from_semantic_scholar tests passed!")
