# sl_sources/__main__.py

import argparse
import asyncio
import json
from . import *

async def main():
    parser = argparse.ArgumentParser(description="Search and download from various sources")
    parser.add_argument("action", choices=["search", "download"], help="Action to perform")
    parser.add_argument("source", choices=["claimminer", "google_scholar", "openalex", "google", "semantic_scholar", "twitter", "youtube"], help="Source to search or download from")
    parser.add_argument("query", help="Search query or ID")
    parser.add_argument("--num_results", type=int, default=10, help="Number of results to return (for search)")
    parser.add_argument("--output", help="Output file for results (optional)")

    args = parser.parse_args()

    if args.action == "search":
        if args.source == "claimminer":
            results = await search_claimminer(args.query, args.num_results)
        elif args.source == "google_scholar":
            results = await search_google_scholar(args.query, args.num_results)
        elif args.source == "openalex":
            results = await search_openalex(args.query, args.num_results)
        elif args.source == "google":
            results = await search_google(args.query, args.num_results)
        elif args.source == "semantic_scholar":
            results = await search_semantic_scholar(args.query, args.num_results)
        elif args.source == "twitter":
            results = await search_twitter(args.query, args.num_results)
        elif args.source == "youtube":
            results = await search_youtube(args.query, args.num_results)
    
    elif args.action == "download":
        if args.source == "google_scholar":
            results = await download_from_google_scholar({"url": args.query})
        elif args.source == "openalex":
            results = await download_from_openalex({"id": args.query})
        elif args.source == "google":
            results = await download_from_google_search({"url": args.query})
        elif args.source == "semantic_scholar":
            results = await download_from_semantic_scholar([{"paperId": args.query}])
        elif args.source == "twitter":
            results = await download_twitter({"tweet_id": args.query})
        elif args.source == "youtube":
            results = await download_from_youtube({"url": args.query})
        else:
            print(f"Download not supported for {args.source}")
            return

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
    else:
        print(json.dumps(results, indent=2))

if __name__ == "__main__":
    asyncio.run(main())