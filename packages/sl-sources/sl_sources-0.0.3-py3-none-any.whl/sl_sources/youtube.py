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


class YoutubeSearch:
    def __init__(self):
        self.url: str
        self.videos: list

    def _parse_html(self, soup_obj: BeautifulSoup):
        video_id = re.search(r"(?<=\?v=)[\w-]+", self.url).group(0)
        title = soup_obj.find("meta", {"name": "title"})["content"]
        thumbnail = f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg"
        js_script = str(soup_obj.find_all("script")[20])
        duration_mil = re.search(r'"approxDurationMs":"(\d+)"', js_script).group(1)
        return {
            "id": video_id,
            "title": title,
            "thumbnail": thumbnail,
            "duration": duration_mil,
        }

    def _fetch_yt_data(self) -> str:
        try:
            response = requests.get(url=self.url)
            response.raise_for_status()
        except requests.RequestException:
            raise requests.RequestException("Failed to fetch data from YouTube.")
        return response.text

    def search_by_url(self, url: str):
        if "https://" in url:
            self.url = url
            response = self._fetch_yt_data()
            soup_obj = BeautifulSoup(response, features="lxml")
            return self._parse_html(soup_obj)
        else:
            raise ValueError("Please provide valid URL.")

    def search_by_term(self, term: str, max_results: int = None):
        encoded_search = urllib.parse.quote_plus(term)
        BASE_URL = "https://youtube.com"
        self.url = f"{BASE_URL}/results?search_query={encoded_search}&sp=CAM"
        response = self._fetch_yt_data()

        results = []
        searched_obj = self._prepare_data(response)
        for contents in searched_obj:
            for video in contents["itemSectionRenderer"]["contents"]:
                res = {}
                if "videoRenderer" in video.keys():
                    video_data = video.get("videoRenderer", {})
                    res["id"] = video_data.get("videoId", None)
                    res["thumbnails"] = [
                        thumb.get("url", None)
                        for thumb in video_data.get("thumbnail", {}).get(
                            "thumbnails", [{}]
                        )
                    ]
                    res["title"] = (
                        video_data.get("title", {})
                        .get("runs", [[{}]])[0]
                        .get("text", None)
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
                    res["duration"] = video_data.get("lengthText", {}).get(
                        "simpleText", 0
                    )
                    res["views"] = video_data.get("viewCountText", {}).get(
                        "simpleText", 0
                    )
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
            self.videos = results
            break
        return results

    def _prepare_data(self, response):
        start = response.index("ytInitialData") + len("ytInitialData") + 3
        end = response.index("};", start) + 1
        json_str = response[start:end]
        data = json.loads(json_str)
        searched_obj = data["contents"]["twoColumnSearchResultsRenderer"][
            "primaryContents"
        ]["sectionListRenderer"]["contents"]

        return searched_obj


async def search_youtube(query: str, num_results: int) -> List[Dict[str, Any]]:
    search_engine = YoutubeSearch()
    search_results = search_engine.search_by_term(query, max_results=num_results)

    results = []
    for search_result in search_results:
        video_id = search_result["id"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        result = {
            "title": search_result["title"],
            "url": video_url,
            "description": search_result["long_desc"],
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


def download_and_process_video(search_result) -> Dict[str, Any]:
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
                return {"full_text": transcript, "url": search_result["url"]}
            except Exception as e:
                print(f"Error reading VTT file: {e}")
        else:
            print("No VTT file found, attempting to transcribe audio with Whisper")
            try:
                id = search_result["url"].split("v=")[1].split("&")[0]
                audio_file = os.path.join(temp_dir, f"{id}")

                def duration_filter(info, *, incomplete):
                    duration = info.get("duration")
                    if duration:
                        if duration > 5400:  # 5400 seconds = 90 minutes
                            return "The video is longer than 90 minutes"
                    return None

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
                    "match_filter": duration_filter,
                }

                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([search_result["url"]])

                if os.path.exists(audio_file + ".mp3"):
                    transcript = transcribe(audio_file + ".mp3")
                    return {"full_text": transcript, "url": search_result["url"]}
                else:
                    print(f"Error: Audio file {audio_file}.mp3 not found.")
                    return {"full_text": None, "url": search_result["url"]}
            except Exception as e:
                print(f"Error in audio transcription: {e}")
                return {"full_text": None, "url": search_result["url"]}


async def download_from_youtube(search_result) -> Dict[str, Any]:
    loop = asyncio.get_running_loop()
    with Pool(processes=1) as pool:
        result = await loop.run_in_executor(
            None, pool.apply, download_and_process_video, (search_result,)
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
    transcripts = await download_videos_parallel(search_results)

    for transcript in transcripts:
        print("transcript")
        print(transcript)

    print("Parallel download and transcription test passed!")


if __name__ == "__main__":
    asyncio.run(main())
