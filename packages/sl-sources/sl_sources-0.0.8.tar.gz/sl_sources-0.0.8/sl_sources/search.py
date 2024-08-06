import asyncio
import hashlib
import json
import os
import traceback
from typing import List

from dotenv import load_dotenv

from .scrape import browser_scrape
import aiohttp

load_dotenv()  # Load environment variables from .env file

GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_API_KEY")
CSE_ID = os.getenv("GOOGLE_CSE_ID")


async def search_google(query, num_results=10, file_type=None):
    results = []
    google_api_url = "https://customsearch.googleapis.com/customsearch/v1"

    params = {
        "key": GOOGLE_SEARCH_API_KEY,
        "cx": CSE_ID,
        "q": query,
        "num": num_results,
    }

    if file_type:
        params["fileType"] = file_type

    async with aiohttp.ClientSession() as session:
        async with session.get(google_api_url, params=params) as response:
            response_json = await response.json()

    if "items" in response_json:
        for item in response_json["items"]:
            title = item.get("title")
            abstract = item.get("snippet")
            url = item.get("link")
            # hash an id from the url
            id = hashlib.md5(url.encode()).hexdigest()
            results.append(
                {
                    "id": id,
                    "title": title,
                    "url": url,
                    "abstract": abstract,
                    "source_type": "google",
                }
            )
    return results



async def download_from_google_search(search_result: List[str]) -> List[str]:
    try:
        search_result["full_text"] = await browser_scrape(search_result["url"])
        return search_result
    except Exception as e:
        print(f"Error scraping {search_result['url']}: {e}")
        print(traceback.format_exc())
        return search_result
    
if __name__ == "__main__":
    query = "Artificial Intelligence"
    num_results = 2

    def search_google_sync():
        # get the loop
        loop = asyncio.get_event_loop()
        # run the search_google function
        search_results = loop.run_until_complete(search_google(query, num_results))
        return search_results

    # Search for results
    search_results = search_google_sync()
    print(f"Search results: {search_results}")

    with open("search_results_google.json", "w") as f:
        json.dump(search_results, f, indent=4, ensure_ascii=False)

    async def run_download_from_google_search(search_results):
        tasks = [download_from_google_search(result) for result in search_results]
        return await asyncio.gather(*tasks)

    # Download pages
    downloaded_pages = asyncio.run(run_download_from_google_search(search_results))
    
    # Save all downloaded pages to ./test_results_google.json
    with open("./download_results_google.json", "w") as f:
        json.dump(downloaded_pages, f, indent=4, ensure_ascii=False)
        
    assert len(search_results) == num_results
    for result in search_results:
        assert all(key in result for key in ["id", "title", "url", "abstract", "source_type"])

    for result in downloaded_pages:
        assert all(key in result for key in ["id", "title", "url", "abstract", "source_type", "full_text"])

    print("search_google and download_from_google_search tests passed!")