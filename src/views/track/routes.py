import requests
import json
from flask import Blueprint, jsonify, session, request
from flask_login import login_required, current_user
from sqlalchemy import delete

from src.extensions import db
from src.models.models import Track, User, user_track
from src.config import Config
from src.functions import token_required

genres_in_file = set()
with open('genres.json', 'r') as f:
    data = json.load(f)
    for genre in data:
        genres_in_file.add(genre['genre'])

track_bp = Blueprint('track', __name__)


@track_bp.route('/like-track/<id>', methods=['POST'])
@login_required
@token_required
def like_track(id):
    name = request.form.get('name')
    artists_name = request.form.get('artists_name')
    artists_id = request.form.get('artists_id')
    album_name = request.form.get('album_name')
    album_id = request.form.get('album_id')
    album_cover = request.form.get('album_cover')
    preview_url = request.form.get('preview_url')
    artists = artists_name.split('/')
    genres_set = set()
    artist_name_for_genre = artists[0].replace(' ', '+')
    track_name_for_genre = name.replace(' ', '+')
    track_tags = requests.get(
        f'http://ws.audioscrobbler.com/2.0/?method=track.gettoptags&artist={artist_name_for_genre}&track={track_name_for_genre}&api_key={Config.LASTFM_KEY}&format=json')
    for genre in track_tags.json()['toptags']['tag']:
        genre = genre['name']
        if 'hip-hop' in genre or 'rnb' in genre:
            genre = genre.replace('-', ' ').replace('rnb', 'r&b')
        if not any(char.isdigit() for char in genre):
            genres_set.add(genre)
    genres = '.'.join(genre for genre in genres_set if genre in genres_in_file)
    genres = '.'.join(genres.split('.')[:3])
    track = Track.query.filter_by(id=id).first()
    if not track:
        track = Track(id=id, name=name, artist_name=artists_name, artist_id=artists_id, album_name=album_name, album_id=album_id,
                      album_cover=album_cover, preview_url=preview_url, genres=genres)
        track.create()
    if track not in current_user.tracks:
        current_user.tracks.append(track)
        current_user.save()
    return jsonify({'message': 'You liked the song.'})


@track_bp.route('/unlike-track/<id>', methods=['POST'])
@login_required
@token_required
def unlike_track(id):
    delete_stmt = delete(user_track).where(
        db.and_(
            user_track.c.user_id == current_user.id,
            user_track.c.track_id == id
        )
    )
    track = Track.query.filter_by(id=id).first()
    track.delete()
    db.session.execute(delete_stmt)
    db.session.commit()
    return jsonify({'message': 'You unliked song.'})