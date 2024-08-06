import asyncio
import os
from typing import Any, Dict, List

from dotenv import load_dotenv
from twikit import Client

load_dotenv()  # Load environment variables from .env file


async def search_twitter(query: str, num_results: int = 10) -> List[Dict[str, Any]]:
    USERNAME = os.getenv("TWITTER_USERNAME")
    EMAIL = os.getenv("TWITTER_EMAIL")
    PASSWORD = os.getenv("TWITTER_PASSWORD")
    client = Client("en-US")
    await client.login(auth_info_1=USERNAME, auth_info_2=EMAIL, password=PASSWORD)
    tweets = await client.search_tweet(query, "Latest")

    results = []
    for tweet in tweets[:num_results]:
        result = {
            "title": f"Tweet by {tweet.user.name}",
            "url": f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}",
            "full_text": tweet.text,
            "created_at": tweet.created_at,
            "tweet_id": tweet.id,
            "source_type": "twitter",
        }
        results.append(result)

    return results


async def download_twitter(tweet_result: Dict[str, Any]) -> Dict[str, Any]:
    USERNAME = os.getenv("TWITTER_USERNAME")
    EMAIL = os.getenv("TWITTER_EMAIL")
    PASSWORD = os.getenv("TWITTER_PASSWORD")
    client = Client("en-US")
    await client.login(auth_info_1=USERNAME, auth_info_2=EMAIL, password=PASSWORD)

    tweet_id = tweet_result["tweet_id"]
    tweet = await client.get_tweet_by_id(tweet_id)

    full_text = tweet.text

    # Get replies to the tweet
    replies = await client.search_tweet(f"to:{tweet.user.screen_name}", "Latest")
    for reply in replies:
        # Check if the reply has a 'in_reply_to_status_id' attribute
        if (
            hasattr(reply, "in_reply_to_status_id")
            and reply.in_reply_to_status_id == tweet_id
        ):
            full_text += f"\n\nReply by {reply.user.name}: {reply.text}"

    # Check if the tweet is a reply to another tweet
    if hasattr(tweet, "in_reply_to_status_id") and tweet.in_reply_to_status_id:
        try:
            parent_tweet = await client.get_tweet_by_id(tweet.in_reply_to_status_id)
            full_text = f"In reply to {parent_tweet.user.name}: {parent_tweet.text}\n\n{full_text}"
        except Exception as e:
            print(f"Error fetching parent tweet: {e}")

    # Check if the tweet is a retweet
    if hasattr(tweet, "retweeted_status") and tweet.retweeted_status:
        try:
            retweeted_tweet = await client.get_tweet_by_id(tweet.retweeted_status.id)
            full_text = f"Retweet of {retweeted_tweet.user.name}: {retweeted_tweet.text}\n\n{full_text}"
        except Exception as e:
            print(f"Error fetching retweeted tweet: {e}")

    result = {
        "title": tweet_result["title"],
        "url": tweet_result["url"],
        "full_text": full_text,
        "created_at": tweet_result["created_at"],
        "source_type": "twitter",
    }

    return result


if __name__ == "__main__":

    async def test_search_twitter():
        query = "Python programming"
        num_results = 3
        results = await search_twitter(query, num_results)

        assert len(results) == num_results

        for result in results:
            assert "title" in result
            assert "url" in result
            assert "full_text" in result
            assert "created_at" in result

        print("search_twitter test passed!")

    async def test_download_twitter():
        query = "Python programming"
        num_results = 1
        search_results = await search_twitter(query, num_results)

        for search_result in search_results:
            downloaded_result = await download_twitter(search_result)

            assert "title" in downloaded_result
            assert "url" in downloaded_result
            assert "full_text" in downloaded_result
            assert "created_at" in downloaded_result

        print("download_twitter test passed!")

    asyncio.run(test_search_twitter())
    asyncio.run(test_download_twitter())
