import requests
from bs4 import BeautifulSoup
import json

def get_video_data(video_url):
    response = requests.get(video_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    script = soup.find_all('script')[3].string
    data = json.loads(script[21:-1])
    return data

def get_hashtags(video_data):
    hashtags = []
    for hashtag in video_data['props']['pageProps']['videoData']['itemInfos']['textExtra']:
        if hashtag['type'] == 'hashtag':
            hashtags.append(hashtag['hashtagName'])
    return hashtags

def get_views(video_data):
    return video_data['props']['pageProps']['videoData']['itemInfos']['playCount']

def get_most_advantageous_hashtag(username):
    url = f"https://www.tiktok.com/@{username}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    video_urls = []
    for video in soup.find_all('a', {'class': 'jsx-1487077427 video-feed-item-wrapper'}):
        video_urls.append(f"https://www.tiktok.com{video['href']}")
    hashtag_counts = {}
    for video_url in video_urls:
        video_data = get_video_data(video_url)
        hashtags = get_hashtags(video_data)
        views = get_views(video_data)
        for hashtag in hashtags:
            if hashtag in hashtag_counts:
                hashtag_counts[hashtag] += views
            else:
                hashtag_counts[hashtag] = views
    return max(hashtag_counts, key=hashtag_counts.get)

username = 'username'
most_advantageous_hashtag = get_most_advantageous_hashtag(username)
print(f"Most Advantageous Hashtag: {most_advantageous_hashtag}")
