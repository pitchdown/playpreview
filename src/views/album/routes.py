import requests
import json
from time import time
from flask import render_template, session, Blueprint, jsonify, request, g
from flask_login import login_required, current_user
from sqlalchemy import exists, delete

from src.extensions import cache, db
from src.functions import get_preview_url_if_null, token_required, get_album_data, get_track_genres
from src.models.models import Track, user_track, Album, user_album
from src.config import Config


genres_in_file = set()
with open('genres.json', 'r') as f:
    data = json.load(f)
    for genre in data:
        genres_in_file.add(genre['genre'])


album_bp = Blueprint('album', __name__)


@album_bp.before_request
def reset_session_tracks():
    if request.path != '/recommendations':
        if ('tracks' or 'genres_list') in session:
            del session['tracks']
            del session['genres_list']


@album_bp.route('/album/<id>')
@login_required
@token_required
def album(id):
    album = Album.query.filter_by(id=id).first()
    check = exists(user_album).where(
        db.and_(
            user_album.c.user_id == current_user.id,
            user_album.c.album_id == id
        )
    )
    result = db.session.query(check).scalar()
    if album:
        artists = [album.artists_name]
        album_data = {
            'name': album.name,
            'id': album.id,
            'artist': artists,
            'artist_id': album.artists_id,
            'cover': album.cover,
            'type': album.type,
            'total_tracks': album.total_tracks,
            'release_date': album.release_date,
        }
        album_data['liked'] = result
        artist_name = album.artists_name.replace(' ', '+')
        album_name = album_data['name'].replace(' ', '+')
    else:
        headers = {
            "Authorization": f"Bearer {session['access_token']}"
        }
        album_data = get_album_data(id, headers)
        album_data['liked'] = result
        g.album_details = album_data
        artist_name = album_data['artist'][0].replace(' ', '+')
        album_name = album_data['name'].replace(' ', '+')
        print(album_data)
        album_exists = Album.query.get(album_data['id']) is not None
        artists_name = '/'.join(artist for artist in album_data['artist'])
        artists_id = ','.join(id for id in album_data['artist_id'])
        if not album_exists:
            album_create = Album(id=album_data['id'], name=album_data['name'], cover=album_data['cover'], type=album_data['type'], total_tracks=album_data['total_tracks'], release_date=album_data['release_date'], artists_name=artists_name, artists_id=artists_id)
            album_create.create()

    response_genres = requests.get(
        f'http://ws.audioscrobbler.com/2.0/?method=album.gettoptags&artist={artist_name}&album={album_name}&api_key={Config.LASTFM_KEY}&format=json')

    genres = []
    if not 'error' in response_genres.json():
        for genre in response_genres.json()['toptags']['tag']:
            genre['name'] = genre['name'].replace('rnb', 'r&b')
            if genre['name'].lower() in genres_in_file and len(genres) < 3:
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
            'artists_name': '/'.join([artist['name'].lower() for artist in track['artists']]),
            'artists_id': ','.join([artist['id'] for artist in track['artists']]),
            'track_number': track['track_number'],
            'preview_url': track.get('preview_url', None) if track.get('preview_url') else get_preview_url_if_null(
                track['id']),
            'album_name': g.album_details['name'],
            'album_id': g.album_details['id'],
            'album_cover': g.album_details['cover'],
        }
        track_data['liked'] = result
        if not track_data['preview_url']:
            track_data['preview_url'] = get_preview_url_if_null(track_data['id'])
        tracks.append(track_data)
        # track_exists = Track.query.get(track_data['id']) is not None
        # artist_name = track_data['artists_name'].replace('/', '+')
        # track_name = track_data['name'].replace(' ', '+')
        # genres = get_track_genres(artist_name, track_name)
        # if not track_exists:
        #     track_create = Track(id=track_data['id'], name=track_data['name'], album_cover=track_data['album_cover'], preview_url=track_data['preview_url'], genres=genres, artist_name=track_data['artists_name'], artist_id=track_data['artists_id'], album_name=track_data['album_name'], album_id=track_data['album_id'])
        #     track_create.create()
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
