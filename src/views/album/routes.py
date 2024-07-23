import requests
import json
from time import time
from flask import render_template, session, Blueprint, jsonify, request, g
from flask_login import login_required, current_user
from sqlalchemy import exists, delete

from src.extensions import cache, db
from src.functions import get_preview_url_if_null, token_required, get_album_data
from src.models.models import Track, user_track, Album, user_album
from src.config import Config


genres_in_file = set()
with open('genres.json', 'r') as f:
    data = json.load(f)
    for genre in data:
        genres_in_file.add(genre['genre'])


album_bp = Blueprint('album', __name__)


@album_bp.route('/album/<id>')
@login_required
@token_required
# @cache.cached(timeout=120)
def album(id):
    headers = {
        "Authorization": f"Bearer {session['access_token']}"
    }
    check = exists(user_album).where(
        db.and_(
            user_album.c.user_id == current_user.id,
            user_album.c.album_id == id
        )
    )
    result = db.session.query(check).scalar()
    album_data = get_album_data(id, headers)
    album_data['liked'] = result
    g.album_details = album_data
    artist_name = album_data['artist'][0].replace(' ', '+')
    album_name = album_data['name'].replace(' ', '+')
    response_genres = requests.get(f'http://ws.audioscrobbler.com/2.0/?method=album.gettoptags&artist={artist_name}&album={album_name}&api_key={Config.LASTFM_KEY}&format=json')
    genres = []
    if not 'error' in response_genres.json():
        for genre in response_genres.json()['toptags']['tag']:
            genre['name'] = genre['name'].replace('rnb', 'r&b')
            if genre['name'].lower() in genres_in_file:
                genres.append(genre['name'].lower())
    return render_template('album/album_page.html', album=album_data, genres=genres)


@album_bp.route('/album/<id>/tracks')
@login_required
@token_required
def album_tracks(id):
    tracks = []
    headers = {
        "Authorization": f"Bearer {session['access_token']}"
    }

    params = {
        'limit': 50
    }

    if not hasattr(g, 'album_details'):
        g.album_details = get_album_data(id, headers)

    response_album_tracks = requests.get(f'https://api.spotify.com/v1/albums/{id}/tracks', headers=headers,
                                         params=params)
    for track in response_album_tracks.json()['items']:
        check = exists().where(
            db.and_(
                user_track.c.user_id == current_user.id,
                user_track.c.track_id == track['id']
            )
        )

        result = db.session.query(check).scalar()
        track_data = {
            'name': track['name'].lower(),
            'id': track['id'],
            'artists_name': [artist['name'] for artist in track['artists']],
            'artists_id': [artist['id'] for artist in track['artists']],
            'track_number': track['track_number'],
            'preview_url': track['preview_url'],
            'album': g.album_details['name'],
            'album_cover': g.album_details['cover'],
        }
        track_data['liked'] = result
        if not track_data['preview_url']:
            track_data['preview_url'] = get_preview_url_if_null(track_data['id'])
        tracks.append(track_data)

    return jsonify(tracks)


@album_bp.route('/like-album/<id>', methods=['POST'])
@login_required
@token_required
def like_album(id):
    name = request.form.get('name')
    artist_id = request.form.get('artist_id')
    cover = request.form.get('cover')
    type = request.form.get('type')
    total_tracks = request.form.get('total_tracks')
    release_date = request.form.get('release_date')
    album = Album.query.filter_by(id=id).first()
    if not album:
        album = Album(id=id, name=name, artist_id=artist_id, cover=cover, type=type, total_tracks=total_tracks,
                      release_date=release_date)
        album.create()
    if album not in current_user.albums:
        current_user.albums.append(album)
        current_user.save()
    return jsonify({'message': 'You liked the album.'})


@album_bp.route('/unlike-album/<id>', methods=['POST'])
@login_required
@token_required
def unlike_album(id):
    delete_stmt = delete(user_album).where(
        db.and_(
            user_album.c.user_id == current_user.id,
            user_album.c.album_id == id
        )
    )
    album = Album.query.filter_by(id=id).first()
    album.delete()
    db.session.execute(delete_stmt)
    db.session.commit()
    return jsonify({'message': 'You unliked album.'})
