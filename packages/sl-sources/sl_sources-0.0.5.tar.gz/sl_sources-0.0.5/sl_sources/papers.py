import re
from typing import Dict, Any
import requests
from bs4 import BeautifulSoup

async def get_paper_details(url: str) -> Dict[str, Any]:
    if "arxiv.org" in url:
        return await get_arxiv_details(url)
    elif "pubmed.ncbi.nlm.nih.gov" in url:
        return await get_pubmed_details(url)
    else:
        raise ValueError("Unsupported URL")

async def get_arxiv_details(url: str) -> Dict[str, Any]:
    arxiv_id = re.search(r'(?:arxiv\.org/abs/)(.+)', url).group(1)
    api_url = f'http://export.arxiv.org/api/query?id_list={arxiv_id}'
    
    async with requests.get(api_url) as response:
        soup = BeautifulSoup(await response.text, 'lxml-xml')
        
        entry = soup.find('entry')
        title = entry.find('title').text
        authors = [author.find('name').text for author in entry.find_all('author')]
        abstract = entry.find('summary').text
        
        return {
            "id": arxiv_id,
            "title": title,
            "authors": authors,
            "abstract": abstract
        }

async def get_pubmed_details(url: str) -> Dict[str, Any]:
    pubmed_id = re.search(r'(?:pubmed\.ncbi\.nlm\.nih\.gov/)(.+)', url).group(1)
    api_url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={pubmed_id}&retmode=json'
    
    async with requests.get(api_url) as response:
        data = await response.json()
        
        result = data['result'][pubmed_id]
        title = result['title']
        authors = result['authors']
        abstract = result['summary']
        
        return {
            "id": pubmed_id,
            "title": title,
            "authors": [f'{author["name"]}' for author in authors],
            "abstract": abstract
        }
    
async def likely_pdf(response):
    try:
        text = await response.text()
        text = text.lower()
        if "invalid article id" in text:
            return False
        if "no paper" in text or "not found" in text:
            return False
        if "404" in text and "error" in text:
            return False
        if "404" in text and "not found" in text:
            return False
        if "403" in text and "forbidden" in text:
            return False
    # Bytestream? Probably a PDF
    except UnicodeDecodeError:
        return True
    # we're still unsure, so let's check mimetype
    if response.headers['Content-Type'] == 'application/pdf' or response.content.startswith(b'%PDF-'):
        return True
    return False


async def pubmed_to_pdf_url(url, session):
    # url = f"https://pubmed.ncbi.nlm.nih.gov/{pubmed_id}/"
    pubmed_id = url.split("/")[-1]

    async with session.get(url) as r:
        if r.status != 200:
            raise Exception(
                f"Error fetching PMC ID for PubMed ID {pubmed_id}. {r.status}"
            )
        html_text = await r.text()
        pmc_id_match = re.search(r"PMC\d+", html_text)
        if pmc_id_match is None:
            raise Exception(f"No PMC ID found for PubMed ID {pubmed_id}.")
        pmc_id = pmc_id_match.group(0)
    pmc_id = pmc_id[3:]

    async with session.get(url) as r:
        if r.status != 200:
            raise Exception(f"No paper with pmc id {pmc_id}. {url} {r.status}")
        html_text = await r.text()
        pdf_url = re.search(r'href="(.*\.pdf)"', html_text)
        if pdf_url is None:
            raise Exception(f"No PDF link found for pmc id {pmc_id}. {url}")
        return f"https://www.ncbi.nlm.nih.gov{pdf_url.group(1)}"

