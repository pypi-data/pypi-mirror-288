import os
from io import BytesIO
from pathlib import Path
import sys
from typing import List

import aiohttp
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from PyPDF2 import PdfReader

load_dotenv()  # Load environment variables from .env file

GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_API_KEY")
CSE_ID = os.getenv("GOOGLE_CSE_ID")

def check_for_playwright():
    if sys.platform.startswith("win"):
        browsers_path = Path(os.getenv("LOCALAPPDATA", "")) / "ms-playwright"
    elif sys.platform == "darwin":
        browsers_path = Path.home() / "Library" / "Caches" / "ms-playwright"
    else:  # Linux and other Unix-like OSes
        browsers_path = Path.home() / ".cache" / "ms-playwright"
    # Search for any folder that contains the word 'chromium'
    chromium_folders = list(browsers_path.glob("*chromium*"))

    if chromium_folders:
        for folder in chromium_folders:
            print("Found chromium folder: ", folder)
        chromium_installed = True
    else:
        print("No chromium folder found")
        chromium_installed = False

    if not chromium_installed:
        print("Browser binaries not found. Installing now...")
        # run playwright install chromium in subprocess
        import subprocess

        result = subprocess.run(
            ["playwright", "install", "chromium"], capture_output=True, text=True
        )
        print("Installation output:")
        print(result.stdout)
        if result.stderr:
            print("Error output:")
            print(result.stderr)
    else:
        print("Browser binaries are already installed.")
    # get the browser path from chromium_folders
    chromium_folders = list(browsers_path.glob("*chromium*"))
    browser_path = chromium_folders[0]
    # if on mac, fine the browser path from the browser_path
    if sys.platform == "darwin":
        browser_path = browser_path / "chrome-mac" / "Chromium.app" / "Contents" / "MacOS" / "Chromium"
    elif sys.platform == "linux":
        browser_path = browser_path / "chrome-linux" / "chrome"
    elif sys.platform == "win32":
        browser_path = browser_path / "chrome-win" / "chrome.exe"
    return browser_path


def search_google(query, num_results=10):
    results = []
    google_api_url = "https://customsearch.googleapis.com/customsearch/v1"

    params = {
        "key": GOOGLE_SEARCH_API_KEY,
        "cx": CSE_ID,
        "q": query,
        "num": num_results,
    }

    response = requests.get(google_api_url, params=params)
    response_json = response.json()

    if "items" in response_json:
        for item in response_json["items"]:
            title = item.get("title")
            snippet = item.get("snippet")
            url = item.get("link")
            results.append(
                {
                    "title": title,
                    "url": url,
                    "snippet": snippet,
                    "source_type": "google",
                }
            )
    return results


scraping_prompt = """
	Analyze this chunk of text and extract clean, coherent, and full quotes. The quotes must come directly from the main content of the article, and your output must be verbatim, exactly as they appear in the text chunk. However, make sure you correct the capitalization at the beginning of each sentence and add a period at the end if it's missing. Follow these guidelines:

	- Return only full, verbatim sentences that reflect the substantive informative content of the original text chunk.
	- Exclude any metadata, website navigational content, disclaimers, captions, advertisements, comments, or non-article elements.
	- Do not include sentence fragments, bullet points, headers, subheaders, footnotes, or incomplete thoughts.
	- Omit interactive phrases such as "Click here", "Share this", or any call-to-action content.
	- Ensure the first letter of each sentence is capitalized, and end each sentence with a period even if it is missing in the source text.
	- Output the resulting parsing as a JSON object with two lists: extracted_quotes and clean_paragraphs

	Do not paraphrase, interpret, or provide summaries. If no sentences in the text chunk meet these criteria, return an empty string. Do not return commentary.

	Here is the text chunk: {text_chunk}
"""

system_instruction = """
	You are a highly refined world-class quote extractor and text cleaner whose job is to analyze chunks of text and extract clean, coherent, and full quotes. 
	The quotes must come directly from the main content of the text, and your output must be verbatim, exactly as they appear in the text chunk. 
	However, make sure you correct the capitalization at the beginning of each sentence and add a period at the end if it's missing. 
	You then take these resulting quotes and format them into paragraphs with logical breaks.

	# You output the resulting quotes in the following JSON format
	{
		"extracted_quotes": [
			"Text parsing begins with the identification of complete sentences within a larger text body.",
			"Each sentence is evaluated for coherence and relevance to the main topic to determine its eligibility for extraction.",
			"Complete sentences that exist as part of a larger set of paragraphs are prioritized for extraction over sentence fragments or headers",
			"You disregard non-substantive content such as what might be found in scraped HTML content or extracted PDF content",
			"Extracted sentences are then corrected for capitalization and punctuation to ensure grammatical accuracy.",
			"Sentences are separated into a json list to maintain clear demarcations between distinct points.",
			"Finally, the cleaned and extracted sentences are compiled into a set of paragraphs, preserving logical sequence and topical flow."
		],
		"clean_paragraphs": [[0, 1, 2], [3, 4], [5, 6]]
	}
"""


def extract_readable_text(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    # Filter out script and style elements
    for unwanted in soup(["script", "style", "header", "footer", "nav", "form"]):
        unwanted.decompose()

    # Define eligible tags that can contain significant content
    content_tags = ["p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "div", "span"]

    # Collect significant text blocks from the HTML content
    text_blocks = []
    for tag in content_tags:
        for element in soup.find_all(tag):
            text = " ".join(element.stripped_strings)
            if text:
                # Append text preserving natural breaks (like paragraphs)
                text_blocks.append(text)

    # Join the text blocks with double newlines to preserve paragraph breaks
    text = "\n\n".join(text_blocks)

    return text


def generate_scraping_prompt(text_chunk):
    return scraping_prompt.replace("{text_chunk}", text_chunk)


def is_pdf_link(url):
    # First, check if the URL ends with .pdf
    if url.lower().endswith(".pdf"):
        return True

    # If it's not clear from the URL, make a HEAD request to inspect headers
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)
        content_type = response.headers.get("Content-Type", "")
        return "application/pdf" in content_type
    except requests.RequestException as e:
        print(f"Failed to send HEAD request to {url}: {e}")
        # An error occurred, you may choose how to handle this.
        return False


async def download_from_google_search(search_result: List[str]) -> List[str]:
    print("download_from_google_search")
    print(f"Scraping {search_result['url']}")
    try:
        search_result["full_text"] = await scrape(search_result["url"])
        return search_result
    except Exception as e:
        print(f"Error scraping {search_result['url']}: {e}")
        return search_result


async def scrape(link: str):
    """
    Asynchronously scrape a source to text chunks
    """

    text = ""

    async def get_text(link):
        from playwright.async_api import async_playwright

        browser_path = check_for_playwright()
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True, executable_path=browser_path)
            page = await browser.new_page()

            await page.goto(link)

            # wait for the page to load
            try:
                await page.wait_for_load_state(state="networkidle", timeout=30000)
            except Exception as e:
                print(f"Error waiting for page to load: {e}")
            text = ""
            try:
                text = await page.content()
            except Exception as e:
                print(f"Error getting page content: {e}")
            await browser.close()
            return text

    if is_pdf_link(link):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(link) as response:
                    content = await response.read()
                    with BytesIO(content) as open_pdf_file:
                        reader = PdfReader(open_pdf_file)
                        text = "\n".join(
                            reader.pages[i].extract_text()
                            for i in range(len(reader.pages))
                        )
            except Exception as e:
                print(f"Error downloading PDF from {link}: {e}")
                text = await get_text(link)
    else:
        text = await get_text(link)

    return text
