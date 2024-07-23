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


def get_preview_url_if_null(id):
    url = f'https://open.spotify.com/embed/track/{id}'
    page = urlopen(url, context=context)
    html_bytes = page.read()
    html = html_bytes.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    script_tag = soup.find('script', id='__NEXT_DATA__')
    json_data = json.loads(script_tag.string)

    audio_preview = json_data.get('props', {}).get('pageProps', {}).get('state', {}).get('data', {}).get('entity', {}).get('audioPreview', {})
    url = audio_preview.get('url')

    if url:
        return url


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