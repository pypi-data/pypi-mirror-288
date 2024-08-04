import asyncio
import hashlib
import aiohttp
import json
import os
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from sl_sources import search_google, search_source
from sl_sources.search import scrape

async def cloud_function_request(request_type, params):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            os.getenv('CLOUD_FUNCTION_URL'),
            json={"type": request_type, **params}
        ) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Error calling cloud function: {response.status}")
                return None
            
async def evaluate_page(text, research_topic, model="gpt-4o-mini"):
    # Load OpenAI API key from environment variable
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', os.getenv('SOCIETY_API_KEY'))
    if not OPENAI_API_KEY:
        raise ValueError("Please set the OPENAI_API_KEY environment variable")
    
    # Truncate text if it's too long (adjust max_length as needed)
    max_length = 128000
    if len(text) > max_length:
        text = text[:max_length] + "..."

    # Prepare the prompt for GPT-4
    prompt = f"""
    Analyze the following text and determine if it's relevant. 
    Also extract any URLs mentioned in the text that seem relevant to these topics.
    
    Text:
    {text}
    
    We are researching the following topic and related domains:
    {research_topic}

    Please evaluate if the text above contains relevant and substantive information for our research.

    Respond with a JSON object containing two fields:
    1. "relevant": a boolean indicating if the text is relevant
    2. "links": a list of relevant URLs extracted from the text which are worth looking at. Ignore links that are not relevant to the research topic.
    3. "summary": a summary of the text, focusing on the most relevant information for the research topic.
    
    Example response:
    {{
        "relevant": true,
        "links": ["https://example.com/ai-article", "https://example.org/ml-study"],
        "summary": "A summary of the text, focusing on the most relevant information for the research topic."
    }}
    """

    # Make API call to OpenAI
    async with aiohttp.ClientSession() as session:
        print("prompt")
        print(prompt)
        async with session.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2
            }
        ) as response:
            if response.status == 200:
                result = await response.json()
                print(result)
                try:
                    evaluation = result['choices'][0]['message']['content']
                    # Remove the ```json and ``` if present
                    evaluation = evaluation.replace('```json\n', '').replace('\n```', '')
                    return json.loads(evaluation)
                except json.JSONDecodeError:
                    print(f"Error parsing GPT-4 response: {result['choices'][0]['message']['content']}")
                    return {"relevant": False, "links": []}
            else:
                print(f"Error calling OpenAI API: {response.status}")
                return {"relevant": False, "links": []}

async def crawl(keywords=[], urls=[], research_topic="", max_depth=3, use_cloud_function=False):
    urls = set(urls) # make sure urls are unique
    keywords = set(keywords) # make sure keywords are unique
    
    youtube_urls = [url for url in urls if "youtube.com" in url] # move any url that contains youtube.com to youtube_urls

    twitter_urls = [url for url in urls if "twitter.com" in url or "x.com" in url] # same for twitter

    # filter urls that are not youtube or twitter
    urls = [url for url in urls if "youtube.com" not in url and "twitter.com" not in url and "x.com" not in url]

    # create a results array for each type
    direct_sources = [{"url": url, "type": "crawl"} for url in urls]
    print("direct_sources")
    print(direct_sources)
    youtube_sources = [{"url": url, "type": "youtube"} for url in youtube_urls]
    print("youtube_sources")
    print(youtube_sources)
    twitter_sources = [{"url": url, "type": "twitter"} for url in twitter_urls]
    print("twitter_sources")
    print(twitter_sources)


    # todo: fix returns on all of these
    sources = [
        # 'google',
        # 'semantic_scholar',
        # 'google_scholar',x
        # 'openalex',
        # 'youtube',
    ]

    search_tasks = []
    num_results = 5

    for source in sources:
        print(f"Queuing keyword searches for source: {source}")
        for keyword in keywords:
            if use_cloud_function:
                task = asyncio.create_task(cloud_function_request("search", {"source": source, "query": keyword, "num_results": num_results}))
            else:
                task = asyncio.create_task(search_source(source, keyword, num_results=num_results))
            search_tasks.append(task)

    search_results = await asyncio.gather(*search_tasks)
    # flatten search_results into a single list
    search_results = [item for sublist in search_results for item in sublist]
    print("search_results")
    print(search_results)

    # join direct_sources, youtube_sources, twitter_sources, and search_results
    sources = direct_sources + youtube_sources + twitter_sources + search_results


    cache = {}
    visited = set()

    async def crawl_links(links, depth):
        if depth > max_depth:
            return
        tasks = []
        for link in links:
            if link not in visited:
                visited.add(link)
                print(f"Crawling {link}")
                task = asyncio.create_task(download_and_evaluate({ "type": "crawl", "url": link }, depth + 1))
                tasks.append(task)
        await asyncio.gather(*tasks)

    if os.path.exists('manifest.json'):
        with open('manifest.json', 'r') as f: 
            cache = json.load(f)

    async def download_and_evaluate(source, depth):
        url = source['url']
        print("url is")
        print(url)
        if depth > max_depth:
            return

        url_hash = hashlib.md5(url.encode()).hexdigest()
        if url_hash in cache:
            # crawl_links the links in the cache
            await crawl_links(cache[url_hash]["links"], depth + 1)
            print(f"Using cached content for {url}")
            return

        try:
            if use_cloud_function:
                # Use cloud function for download
                result = await cloud_function_request("download", {"search_result": {"url": url, "search_type": "crawl"}})
                if not result:
                    return
                content = result.get('full_text', '')
            else:
                content = await scrape(url)

            result = await evaluate_page(content, research_topic)
            print("result")
            print(result)
            if result["relevant"]:
                file_name = f"{url_hash}.txt"
                file_path = os.path.join("./downloaded_data", file_name)
                
                os.makedirs("./downloaded_data", exist_ok=True)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                cache[url_hash] = {
                    "url": url,
                    "file_path": file_path,
                    "links": result["links"],
                    "summary": result["summary"],
                    "relevant": result["relevant"]
                }
                
                with open('manifest.json', 'w') as f:
                    json.dump(cache, f, indent=2)
                
                await crawl_links(result["links"], depth + 1)
            else:
                cache[url_hash] = {
                    "url": url,
                    "links": result["links"],
                    "summary": result["summary"],
                    "relevant": result["relevant"]
                }
        except Exception as e:
            print(f"Error crawling {url}: {e}")

    tasks = []
    for source in sources:
        print("source is")
        print(source)
        print(f"Crawling {source['url']}")
        visited.add(source['url'])
        task = asyncio.create_task(download_and_evaluate(source, 0))
        tasks.append(task)

    await asyncio.gather(*tasks)

async def main():
    research_topic = "can humans keep up? the impact of artificial intelligence on neuroscience"
    keywords = ["artificial intelligence", "machine learning", "neuroscience and the ai race"]
    urls = ["https://www.neuralink.com", "https://www.openai.com", "https://www.anthropic.com", "https://www.lesswrong.com/posts/4sEK5mtDYWJo2gHJn/catastrophic-risks-from-ai-3-ai-race"]
    
    use_cloud_function = os.getenv('CLOUD_FUNCTION_ENABLED', 'false').lower() == 'true'
    await crawl(keywords, urls, research_topic=research_topic, max_depth=2, use_cloud_function=use_cloud_function)
    
    print("Crawl completed. Check the 'downloaded_data' directory and 'manifest.json' for results.")

if __name__ == "__main__":
    asyncio.run(main())
