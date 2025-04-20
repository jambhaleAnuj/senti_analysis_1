from dotenv import load_dotenv
import os
from googleapiclient.discovery import build
from datetime import datetime


load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API")

yt = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)


def search_trailer_video_id(movie_title):
    search_response = yt.search().list(
        q=f"{movie_title} official trailer",
        part="snippet",
        type="video",
        maxResults=1
    ).execute()

    if not search_response["items"]:
        return None
    return search_response["items"][0]["id"]["videoId"]

def get_trailer_comments(movie_title, max_pages=3):
    # videos_search = VideosSearch(f"{movie_title} official trailer", limit=1)
    # video_id = videos_search.result()['result'][0]['id']
    video_id = search_trailer_video_id(movie_title)
    comments = []
    next_page_token = None

    for _ in range(max_pages):  # simulate going deeper into older comments
        response = yt.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            textFormat="plainText",
            order="time",  # get comments sorted by NEWEST first
            pageToken=next_page_token
        ).execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append({
                'text': comment['textDisplay'],
            })
            # print(comments)
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    # Reverse to simulate oldest first
    comments.reverse()
    return comments
