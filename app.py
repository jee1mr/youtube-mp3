from flask import Flask, request, jsonify, render_template, send_from_directory
from urllib import unquote_plus
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import youtube_dl
from config import DEVELOPER_KEY # create a config.py with that constant

app = Flask(__name__, static_url_path='/static')

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/search')
def search():
    urlencoded_keyword = request.args.get('q')
    keyword = unquote_plus(urlencoded_keyword) if urlencoded_keyword else ''
    max_results = 10
    videos = []

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
      developerKey=DEVELOPER_KEY)

    search_response = youtube.search().list(
      q=keyword,
      part='id,snippet',
      maxResults=max_results
    ).execute()

    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            video = {
            	'title': search_result['snippet']['title'],
            	'thumbnail': search_result['snippet']['thumbnails']['default']['url'],
            	'videoId': search_result['id']['videoId']
            }
            videos.append(video)

    return jsonify(videos)

@app.route('/convert/<videoId>')
def convert(videoId):
    print "convert(): " + videoId
    url = 'https://www.youtube.com/watch?v=' + videoId
    ydl_opts['outtmpl'] = 'temp/' + videoId + '.mp3'
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    result = { 'downloadUrl' : "/download/" + videoId + ".mp3" }
    return jsonify(result)

@app.route('/download/<path:path>')
def download(path):
    return send_from_directory('temp', path);

def ymp3_progress_hooks(e):
    print e['status']
    if e['status'] == 'finished':
        print('Done downloading, now converting ...')

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'progress_hooks': [ymp3_progress_hooks],
}

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=8000)
