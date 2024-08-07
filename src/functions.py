import requests
import ssl
import certifi
import json
from functools import wraps
from urllib.request import urlopen
from bs4 import BeautifulSoup
from flask import url_for, redirect, session
from time import time
from datetime import datetime

from src.config import Config

context = ssl.create_default_context(cafile=certifi.where())


genres_in_file = set()
with open('genres.json', 'r') as f:
    data = json.load(f)
    for genre in data:
        genres_in_file.add(genre['genre'])


def get_preview_url_if_null(id):
    url = f'https://open.spotify.com/embed/track/{id}'
    page = urlopen(url, context=context)
    html_bytes = page.read()
    html = html_bytes.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    script_tag = soup.find('script', id='__NEXT_DATA__')
    json_data = json.loads(script_tag.string)

    audio_preview = json_data['props']['pageProps']['state']['data']['entity']['audioPreview']['url']
    return audio_preview


def get_album_data(id, headers):
    response_album = requests.get(f'https://api.spotify.com/v1/albums/{id}', headers=headers)
    album_data = response_album.json()

    return {
        'name': album_data['name'].lower(),
        'id': album_data['id'],
        'artist': [artist['name'].lower() for artist in album_data['artists']],
        'artist_id': [artist['id'] for artist in album_data['artists']],
        'cover': album_data['images'][0]['url'],
        'type': album_data['album_type'],
        'total_tracks': album_data['total_tracks'],
        'release_date': album_data['release_date'],
        'url': album_data['external_urls']['spotify'],
    }


def get_track_genres(artist_name, track_name):
    genres_set = set()
    print(artist_name, track_name, '<---- functions.py')
    track_tags = requests.get(
        f'http://ws.audioscrobbler.com/2.0/?method=track.gettoptags&artist={artist_name}&track={track_name}&api_key={Config.LASTFM_KEY}&format=json')
    if track_tags.json()['toptags']['tag']:
        for genre in track_tags.json()['toptags']['tag']:
            genre = genre['name']
            if 'hip-hop' in genre or 'rnb' in genre:
                genre = genre.replace('-', ' ').replace('rnb', 'r&b')
            if not any(char.isdigit() for char in genre):
                genres_set.add(genre)
    else:
        url = f'https://www.last.fm/music/{artist_name_for_genre}/_/{track_name_for_genre}'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        tags_section = soup.find("ul", class_="tags-list")
        if tags_section:
            tags = [tag.text.strip() for tag in tags_section.find_all("li")]
            for genre in tags:
                if 'hip-hop' in genre or 'rnb' in genre:
                    genre = genre.replace('-', ' ').replace('rnb', 'r&b')
                if not any(char.isdigit() for char in genre):
                    genres_set.add(genre)
    genres = '.'.join(genre for genre in genres_set if genre in genres_in_file)
    genres = '.'.join(genres.split('.')[:3])
    return genres


def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'access_token' not in session:
            return redirect(url_for('auth.sign_in'))
        if 'access_token' in session and session['expire_time'] <= time():
            data = {
                'client_id': Config.CLIENT_ID,
                'client_secret': Config.CLIENT_SECRET,
                'grant_type': 'client_credentials'
            }
            response = requests.post(Config.TOKEN_URL, data=data)
            if response.status_code == 200:
                session['access_token'] = response.json()['access_token']
                session['expire_time'] = datetime.now().timestamp() + response.json()['expires_in']
            else:
                return redirect(url_for('auth.sign_in'))
        return f(*args, **kwargs)
    return wrapper