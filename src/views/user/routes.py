from flask import Blueprint, session, render_template, redirect, url_for, jsonify
from flask_login import current_user, login_required
from sqlalchemy import exists
from collections import Counter

from src.models.models import User, Artist, Album, Track, user_artist, user_album, user_track
from src.extensions import db
from src.functions import token_required


user_bp = Blueprint('user', __name__)


@user_bp.route('/<name>')
def profile(name):
    user = User.query.filter_by(username=name).first()
    if not user:
        return jsonify({'message': "User doesn't exists"})
    favorite_genres = Counter()
    recently_liked_tracks = []
    recently_liked_artists = []
    for track in user.tracks:
        genres = track.genres.split('.')
        favorite_genres.update(genres)
        recently_liked_tracks.append(track)
    favorite_genres = list(dict(favorite_genres.most_common()))[:5]
    for artist in user.artists:
        recently_liked_artists.append(artist)
    # artists_data = db.session.query(user_artist).all()
    # recently_liked_artists = artists_data[-4:]
    # recently_liked_artists_ids = [artist[1] for artist in reversed(recently_liked_artists)]
    # artists = Artist.query.filter(Artist.id.in_(recently_liked_artists_ids)).all()
    # favorite_artists = db.session.query(user_artist).where(user_artist.c.user_id == user.id, user_artist.c.favorited == True).order_by(user_artist.c.order).all()
    # favorite_artists_ids = [id for _, id, _, _ in favorite_artists]
    # favorite_artists_data = Artist.query.filter(Artist.id.in_(favorite_artists_ids)).all()
    # for artist in favorite_artists_data:
    #     print(artist.name)
    # favorite_albums = db.session.query(user_album).where(user_album.c.user_id == user.id, user_album.c.favorited == True).order_by(user_album.c.order).all()
    # favorite_albums_ids = [id for _, id, _, _ in favorite_albums]
    # favorite_albums_data = Album.query.filter(Album.id.in_(favorite_albums_ids)).all()
    # for album in favorite_albums_data:
    #     print(album.name)
    return render_template('/user/profile.html', username=name, genres=favorite_genres, tracks=reversed(recently_liked_tracks[-4:]), artists=reversed(recently_liked_artists[-4:]))


@user_bp.route('/favorite-artist/<id>')
@login_required
@token_required
def favorite_artist(id):
    artist = Artist.query.filter_by(id=id).first()
    print(artist)
    return jsonify({'message': 'You favorited an artist.'})