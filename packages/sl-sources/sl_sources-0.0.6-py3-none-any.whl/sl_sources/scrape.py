import os
from io import BytesIO
from pathlib import Path
import random
import sys
import time

import aiohttp
from bs4 import BeautifulSoup, NavigableString
from PyPDF2 import PdfReader

import os
from pathlib import Path
import sys
import asyncio

from typing import Optional

link_blacklist = [
    "home",
    "next",
    "about us",
    "contact",
    "log in",
    "account",
    "sign",
    "sign up",
    "sign in",
    "sign out",
    "privacy",
    "close",
    "privacy policy",
    "terms of service",
    "terms and conditions",
    "terms",
    "conditions",
    "privacy",
    "legal",
    "guidelines",
    "filter",
    "theme",
    "english",
    "accessibility",
    "authenticate",
    "join",
    "edition",
    "subscribe",
    "news",
    "home",
    "blog",
    "jump to",
    "español",
    "world",
    "europe",
    "politics",
    "profile",
    "election",
    "health",
    "business",
    "tech",
    "sports",
    "advertise",
    "advertising",
    "ad",
    "banner",
    "sponsor",
    "promotion",
    "promoted",
]


element_blacklist = [
    "sidebar",
    "nav",
    "footer",
    "header",
    "menu",
    "account",
    "login",
    "form",
    "search",
    "advertisement",
    "masthead",
    "popup",
    "overlay",
    "floater",
    "modal",
    "noscript",
    "iframe",
    "script",
    "style",
    "head",
    "meta"
]

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

async def get_browser_and_page(playwright, capsolver_api_key=None):
    browser_path = check_for_playwright()

    from playwright_stealth import stealth_async
    # check if CAPSOLVER_API_KEY exists
    if capsolver_api_key is None:
        capsolver_api_key = os.getenv("CAPSOLVER_API_KEY")
    
    if capsolver_api_key is None or capsolver_api_key == "":
        print("Warning: No capsolver API key provided. Attempting to launch browser without a captcha solver")

    from capsolver_extension_python import Capsolver
    extension_path = Capsolver(api_key=capsolver_api_key).load(with_command_line_option=False) 
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    browser = await playwright.chromium.launch(headless=True, executable_path=browser_path, args=[
            '--disable-extensions-except='+ extension_path,
            '--load-extension=' + extension_path,
            '--user-agent=' + user_agent,
        ])
    page = await browser.new_page()
    await stealth_async(page)
    return browser, page

async def extract_plain_text(page):
    content = await page.content()
    soup = BeautifulSoup(content, 'html.parser')
    
    # Remove scripts and style elements
    for element in soup(['script', 'style']):
        element.decompose()

    # Define blacklists
    link_blacklist = ['unwanted_link_keyword1', 'unwanted_link_keyword2']  # Adjust as needed

    # Remove blacklisted links
    for link in soup.find_all('a'):
        href = link.get('href', '').lower()
        text = link.text.lower()
        if any(keyword in href or keyword in text for keyword in link_blacklist):
            link.decompose()

    # Define inline and block elements
    inline_elements = {'span', 'a', 'button', 'strong', 'em', 'i', 'b', 'small', 'code'}
    block_elements = {'div', 'main', 'section', 'article', 'section', 'p', 'li', 'ol', 'ul', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote'}
    
    # Function to recursively process elements
    def process_element(element):
        if isinstance(element, NavigableString):  # Check if the element is a NavigableString
            return element.strip()
        
        if element.name in inline_elements:
            return ' ' + ' '.join(process_element(child) for child in element.children if child.name != 'br').strip() + ' '
        elif element.name in block_elements:
            return '\n' + '\n'.join(process_element(child) for child in element.children).strip() + '\n'
        else:
            return ' '.join(process_element(child) for child in element.children).strip()

    text = process_element(soup.body or soup)  # Start processing from body or root
    text = ' '.join(text.split())  # Normalize whitespace
    text = text.replace(' \n ', '\n').replace('\n ', '\n').replace(' \n', '\n').strip()  # Final cleanup
    
    return text


def resolve_with_wayback_machine(link: str) -> str:
    from waybackpy import Url
    user_agent = "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0"
    wayback_url = Url(link, user_agent)
    wayback_url.newest()
    url = wayback_url.archive_url
    return url

wayback_resolution_whitelist = [
    "nytimes",
    "wsj",
    "nyt",
    "latimes",
    "washingtonpost",
    "bbc",
    "cnn",
    "foxnews",
    "nbcnews",
    "cnbc",
    "reuters",
    "apnews",
    "bloomberg",
    "businessinsider",
    "businesswire",
    "theverge"
]

async def browser_scrape(link: str) -> str:
    """
    Asynchronously scrape a source to extract text.
    
    Args:
    link (str): The URL of the webpage to scrape.

    Returns:
    str: The extracted text content from the webpage.
    """
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        try:
            browser, page = await get_browser_and_page(p)
            if any(keyword in link for keyword in wayback_resolution_whitelist):
                new_link = resolve_with_wayback_machine(link)
                link = new_link if new_link else link
            await page.goto(link, wait_until="networkidle")
            # wait for 2 seconds to defeat any captchas etc
            await asyncio.sleep(2)
            extracted_text = await extract_plain_text(page)
            return extracted_text
        except Exception as e:
            print(f"Error during scraping: {e}")
            # if we've already wayback machine'd it, don't try again
            if any(keyword in link for keyword in wayback_resolution_whitelist):
                return ""
            # try to resolve with wayback machine
            new_link = resolve_with_wayback_machine(link)
            if new_link and new_link != link:
                return await browser_scrape(new_link)
            else:
                return ""
        finally:
            await browser.close()


if __name__ == "__main__":
    import asyncio
    async def run():
        print("Scraping...")
        text = await browser_scrape("https://www.nytimes.com/2024/04/29/technology/ai-google-microsoft.html")
        print("Scraped")
        print(text)

    asyncio.run(run())