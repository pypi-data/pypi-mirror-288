from .claimminer import search_claimminer
from .search import download_from_google_search, search_google
from .google_scholar import download_from_google_scholar, search_google_scholar
from .openalex import download_from_openalex, search_openalex
from .semantic_scholar import download_from_semantic_scholar, search_semantic_scholar
from .twitter import search_twitter
from .youtube import download_from_youtube, search_youtube

CHUNK_SIZE = 5


async def search_source(source, query, num_results):
    if source == "google":
        print("Searching Google")
        results = await search_google(query, num_results=num_results)
        print(f"Found {len(results)} results from Google")
        return results
    elif source == "semantic_scholar":  # arxiv, pubmed, sagepub
        print("Searching Semantic Scholar")
        results = await search_semantic_scholar(query, num_results=num_results)
        print(f"Found {len(results)} results from Semantic Scholar")
        return results
    elif source == "twitter":
        print("Searching Twitter")
        results = await search_twitter(query, num_results)
        print(f"Found {len(results)} results from Twitter")
        return results
    elif source == "youtube":
        print("Searching Youtube")
        results = await search_youtube(query, num_results=num_results)
        print(f"Found {len(results)} results from Youtube")
        return results
    elif source == "google_scholar":
        print("Searching Google Scholar")
        results = await search_google_scholar(query, num_results=num_results)
        print(f"Found {len(results)} results from Google Scholar")
        return results
    elif source == "openalex":
        print("Searching OpenAlex")
        results = await search_openalex(query, num_results=num_results)
        print(f"Found {len(results)} results from OpenAlex")
        return results
    elif source == "claimminer":
        claimminer_results = await search_claimminer(query, cutoff=0.7)
        print(f"Found {len(claimminer_results)} results from ClaimMiner")
        return claimminer_results
    else:
        return []


async def download_source(search_result):
    print(f"Downloading {search_result['url']}")
    source_type = search_result.get("source_type", "crawl")
    if source_type == "crawl":
        # scrapes the url directly
        result = await download_from_google_search(search_result)
    elif source_type == "google":
        result = await download_from_google_search(search_result)
    elif source_type == "twitter":
        result = search_result
    elif source_type == "youtube":
        result = await download_from_youtube(search_result)
    elif source_type == "google_scholar":
        result = await download_from_google_scholar(search_result)
    elif source_type == "semantic_scholar":
        result = await download_from_semantic_scholar(search_result)
    elif source_type == "openalex":
        result = await download_from_openalex(search_result)
    else:
        result = search_result

    return result
