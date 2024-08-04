import asyncio
import io
from typing import Any, Dict, List

import aiohttp
from bs4 import BeautifulSoup
from pyalex import Works
from PyPDF2 import PdfReader

from .search import scrape


async def search_openalex(query: str, num_results: int) -> List[Dict[str, Any]]:
    print("query")
    print(query)
    results = []

    works = (
        Works()
        .search(query)
        .select(["id", "doi", "title", "publication_year", "cited_by_count"])
        .paginate(per_page=num_results)
    )

    for page in works:
        for work in page:
            result = {
                "id": work.get("id"),
                "doi": work.get("doi"),
                "title": work.get("title"),
                "publication_year": work.get("publication_year"),
                "cited_by_count": work.get("cited_by_count"),
                "url": f"https://doi.org/{work['doi']}" if work.get("doi") else None,
                "source_type": "openalex",
            }

            full_work = Works()[work["id"]]
            result["abstract"] = full_work.get("abstract")

            results.append(result)

        if len(results) >= num_results:
            break

    return results[:num_results]


async def download_and_extract_text(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                content_type = response.headers.get("Content-Type", "").lower()
                if "application/pdf" in content_type:
                    # If it's already a PDF, process it
                    pdf_content = await response.read()
                else:
                    # If it's not a PDF, try to find a PDF link
                    html_content = await response.text()
                    soup = BeautifulSoup(html_content, "html.parser")
                    pdf_link = None
                    for a in soup.find_all("a", href=True):
                        if a["href"].lower().endswith(".pdf"):
                            pdf_link = a["href"]
                            break

                    if not pdf_link:
                        return await scrape(url)

                    # If the PDF link is relative, make it absolute
                    if not pdf_link.startswith("http"):
                        pdf_link = (
                            f"{response.url.scheme}://{response.url.host}{pdf_link}"
                        )

                    # Download the PDF
                    async with session.get(pdf_link) as pdf_response:
                        if pdf_response.status == 200:
                            pdf_content = await pdf_response.read()
                        else:
                            return await scrape(url)

                # Process the PDF content
                pdf_file = io.BytesIO(pdf_content)
                pdf_reader = PdfReader(pdf_file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
            else:
                return f"Failed to access the URL. Status code: {response.status}"


async def download_from_openalex(search_result) -> Dict[str, Any]:
    id = search_result["id"]
    work = Works()[id]

    print("work")
    print(work)

    result = {
        "id": work.get("id"),
        "doi": work.get("doi"),
        "title": work.get("title"),
        "url": f"https://doi.org/{work['doi']}" if work.get("doi") else work.get("id"),
        "full_text": None,
        "source_type": "openalex",
    }
    if result["url"].startswith("https://doi.org/"):
        result["full_text"] = await download_and_extract_text(result["url"])

    return result


if __name__ == "__main__":

    async def test_search_openalex():
        query = "Artificial Intelligence"
        num_results = 3
        results = await search_openalex(query, num_results)

        assert len(results) == num_results

        for result in results:
            assert "id" in result
            assert "doi" in result
            assert "title" in result
            assert "abstract" in result
            assert "publication_year" in result
            assert "cited_by_count" in result
            assert "url" in result

        print("search_openalex test passed!")

    async def test_download_from_openalex():
        paper_id = "W2741809807"
        result = await download_from_openalex(paper_id)

        assert "id" in result
        assert "doi" in result
        assert "title" in result
        assert "url" in result
        assert "full_text" in result

        print("download_from_openalex test passed!")

    asyncio.run(test_download_from_openalex())
    asyncio.run(test_search_openalex())
