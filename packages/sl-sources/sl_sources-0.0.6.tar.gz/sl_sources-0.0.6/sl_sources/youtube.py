import asyncio
import glob
import json
import os
import re
import tempfile
import urllib.parse
from multiprocessing import Pool
from typing import Any, Dict, List

import requests
from bs4 import BeautifulSoup
from yt_dlp import YoutubeDL
import librosa


def fetch_youtube_data(url) -> str:
    try:
        response = requests.get(url=url)
        response.raise_for_status()
    except requests.RequestException:
        raise requests.RequestException("Failed to fetch data from YouTube.")
    return response.text


def search_by_url(url: str):
    if "https://" in url:
        response = fetch_youtube_data(url)
        soup_obj = BeautifulSoup(response, features="lxml")
        video_id = re.search(r"(?<=\?v=)[\w-]+", url).group(0)
        title = soup_obj.find("meta", {"name": "title"})["content"]
        js_script = str(soup_obj.find_all("script")[20])
        duration_mil = re.search(r'"approxDurationMs":"(\d+)"', js_script).group(1)
        description = soup_obj.find("meta", {"name": "description"})["content"]
        if description is None:
            # find the ytd-text-inline-expander" elemenent and get all the text
            description = soup_obj.find("ytd-text-inline-expander").get_text()


        return {
            "id": video_id,
            "title": title,
            "url": url,
            "duration": duration_mil,
            "long_desc": description,
        }
    else:
        raise ValueError("Please provide valid URL.")


def search_by_term(term: str, max_results: int = None):
    encoded_search = urllib.parse.quote_plus(term)
    BASE_URL = "https://youtube.com"
    url = f"{BASE_URL}/results?search_query={encoded_search}&sp=CAM"
    response = fetch_youtube_data(url)

    results = []
    searched_obj = _prepare_data(response)
    for contents in searched_obj:
        for video in contents["itemSectionRenderer"]["contents"]:
            res = {}
            if "videoRenderer" in video.keys():
                video_data = video.get("videoRenderer", {})
                res["id"] = video_data.get("videoId", None)
                res["thumbnails"] = [
                    thumb.get("url", None)
                    for thumb in video_data.get("thumbnail", {}).get("thumbnails", [{}])
                ]
                res["title"] = (
                    video_data.get("title", {}).get("runs", [[{}]])[0].get("text", None)
                )
                res["long_desc"] = (
                    video_data.get("descriptionSnippet", {})
                    .get("runs", [{}])[0]
                    .get("text", None)
                )
                
                res["channel"] = (
                    video_data.get("longBylineText", {})
                    .get("runs", [[{}]])[0]
                    .get("text", None)
                )
                res["duration"] = video_data.get("lengthText", {}).get("simpleText", 0)
                res["views"] = video_data.get("viewCountText", {}).get("simpleText", 0)
                res["publish_time"] = video_data.get("publishedTimeText", {}).get(
                    "simpleText", 0
                )
                res["url_suffix"] = (
                    video_data.get("navigationEndpoint", {})
                    .get("commandMetadata", {})
                    .get("webCommandMetadata", {})
                    .get("url", None)
                )
                results.append(res)

        if results:
            if max_results is not None and len(results) > max_results:
                return results[:max_results]
        break
    return results


def _prepare_data(response):
    start = response.index("ytInitialData") + len("ytInitialData") + 3
    end = response.index("};", start) + 1
    json_str = response[start:end]
    data = json.loads(json_str)
    searched_obj = data["contents"]["twoColumnSearchResultsRenderer"][
        "primaryContents"
    ]["sectionListRenderer"]["contents"]

    return searched_obj


async def search_youtube(query: str, num_results: int) -> List[Dict[str, Any]]:
    search_results = search_by_term(query, max_results=num_results)

    results = []
    for search_result in search_results:
        video_id = search_result["id"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        video_data = search_by_url(video_url)

        result = {
            "id": video_id,
            "title": search_result["title"],
            "abstract": search_result["long_desc"] or video_data["long_desc"],
            "year": search_result["publish_time"][
                :4
            ],  # Extract the year from publish_time
            "authors": [search_result["channel"]],
            "url": video_url,
            "source_type": "youtube",
        }
        results.append(result)

    return results


def download_video(url, temp_dir):
    ydl_opts = {
        "overwrites": True,
        "format": "bestaudio",
        "outtmpl": os.path.join(temp_dir, "audio.mp3"),
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)
        return os.path.join(temp_dir, "audio.mp3")


def format_timestamp(
    seconds: float, always_include_hours: bool = False, decimal_marker: str = "."
):
    if seconds is not None:
        milliseconds = round(seconds * 1000.0)
        hours = milliseconds // 3_600_000
        milliseconds -= hours * 3_600_000
        minutes = milliseconds // 60_000
        milliseconds -= minutes * 60_000
        seconds = milliseconds // 1_000
        milliseconds -= seconds * 1_000
        hours_marker = f"{hours:02d}:" if always_include_hours or hours > 0 else ""
        return f"{hours_marker}{minutes:02d}:{seconds:02d}{decimal_marker}{milliseconds:03d}"
    else:
        return seconds


from tqdm import tqdm


def transcribe(audio_file):
    from transformers import WhisperProcessor, WhisperForConditionalGeneration

    processor = WhisperProcessor.from_pretrained("openai/whisper-tiny.en")
    model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny.en")

    # Load the audio file using librosa
    audio_data, sampling_rate = librosa.load(audio_file)

    # Resample the audio to 16000 Hz
    resampled_audio = librosa.resample(
        audio_data, orig_sr=sampling_rate, target_sr=16000
    )

    # Define chunk size (in seconds)
    chunk_length_s = 30
    chunk_length_samples = chunk_length_s * 16000  # 16000 is the target sampling rate

    # Split audio into chunks
    audio_chunks = [
        resampled_audio[i : i + chunk_length_samples]
        for i in range(0, len(resampled_audio), chunk_length_samples)
    ]

    transcription = []

    # Process each chunk
    for chunk in tqdm(audio_chunks, desc="Transcribing"):
        inputs = processor(chunk, sampling_rate=16000, return_tensors="pt")

        if "input_features" in inputs:
            input_features = inputs["input_features"]
        else:
            raise ValueError("The processor output does not contain 'input_features'.")

        outputs = model.generate(
            input_features,
            output_scores=False,
            return_dict_in_generate=True,
            output_attentions=False,
        )

        for sequence in outputs.sequences:
            chunk_text = processor.decode(sequence, skip_special_tokens=True)
            transcription.append(chunk_text)

    full_transcription = " ".join(transcription)
    return full_transcription


def download_from_youtube_sync(search_result) -> Dict[str, Any]:
    print(f"Downloading video from youtube: {search_result['url']}")

    with tempfile.TemporaryDirectory() as temp_dir:
        ydl_opts = {
            "writesubtitles": True,
            "subtitleslangs": ["en"],
            "subtitlesformat": "vtt",
            "outtmpl": os.path.join(temp_dir, "%(title)s.%(ext)s"),
            "skip_download": True,
            "quiet": False,
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([search_result["url"]])

        vtt_files = glob.glob(os.path.join(temp_dir, "*.vtt"))
        if vtt_files:
            vtt_file = vtt_files[0]
            try:
                with open(vtt_file, "r", encoding="utf-8") as f:
                    vtt_data = f.read()
                transcript = vtt_to_text(vtt_data)
                search_result["full_text"] = transcript
                return search_result
            except Exception as e:
                print(f"Error reading VTT file: {e}")
        else:
            print("No VTT file found, attempting to transcribe audio with Whisper")
            try:
                id = search_result["url"].split("v=")[1].split("&")[0]
                audio_file = os.path.join(temp_dir, f"{id}")

                # def duration_filter(info, *, incomplete):
                #     duration = info.get("duration")
                #     if duration:
                #         if duration > 6000:  # 5400 seconds = 100 minutes
                #             return "The video is longer than 100 minutes"
                #     return None

                ydl_opts = {
                    "format": "bestaudio/best",
                    "outtmpl": audio_file,
                    "postprocessors": [
                        {
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": "mp3",
                            "preferredquality": "192",
                        }
                    ],
                    # "match_filter": duration_filter,
                }

                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([search_result["url"]])

                if os.path.exists(audio_file + ".mp3"):
                    transcript = transcribe(audio_file + ".mp3")
                    search_result["full_text"] = transcript
                    return search_result
                else:
                    print(f"Error: Audio file {audio_file}.mp3 not found.")
                    search_result["full_text"] = None
                    return search_result
            except Exception as e:
                print(f"Error in audio transcription: {e}")
                search_result["full_text"] = None
                return search_result


async def download_from_youtube(search_result) -> Dict[str, Any]:
    # run async on a separate thread so it doesn't block the main thread
    loop = asyncio.get_running_loop()
    with Pool(processes=1) as pool:
        result = await loop.run_in_executor(
            None, pool.apply, download_from_youtube_sync, (search_result,)
        )
    return result


def vtt_to_text(vtt_data: str) -> str:
    print("Converting VTT to text")
    lines = vtt_data.strip().split("\n")
    transcript = []

    for line in lines[2:]:  # Skip the first two lines (WEBVTT and blank line)
        if "-->" not in line and not line.strip().isdigit():
            transcript.append(line.strip())

    return " ".join(transcript)


async def test_search_youtube():
    query = "Python tutorial"
    num_results = 2
    results = await search_youtube(query, num_results)

    assert len(results) == num_results

    for result in results:
        assert "title" in result
        assert "url" in result
        assert "description" in result

    print("Test passed!")


async def test_download_and_transcribe():
    # Test video without captions
    video_url_no_captions = {"url": "https://www.youtube.com/watch?v=xuCn8ux2gbs"}
    transcript_no_captions = await download_from_youtube(video_url_no_captions)
    assert transcript_no_captions, "Failed to transcribe video"
    print("Successfully transcribed video")

    # Add assertions to check the content of the transcripts
    assert (
        len(transcript_no_captions.get("full_text", "").split()) > 100
    ), "Transcript seems too short"


async def download_videos_parallel(search_results):
    tasks = [download_from_youtube(result) for result in search_results]
    gathered = await asyncio.gather(*tasks)
    return gathered


async def main():
    # Test parallel downloading
    query = "self introduction"
    num_results = 3
    search_results = await search_youtube(query, num_results)
    # save search results to youtube_search.json
    with open("youtube_search.json", "w") as f:
        json.dump(search_results, f)

    download_results = await download_videos_parallel(search_results)

    # save download results
    with open("youtube_download.json", "w") as f:
        json.dump(download_results, f)

    print("Parallel download and transcription test passed!")


if __name__ == "__main__":
    asyncio.run(main())
