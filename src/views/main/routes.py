import requests
from random import choice
from flask import Blueprint, render_template, session, request
from flask_login import login_required, current_user
from collections import Counter

from src.extensions import db
from src.models.models import Track, Artist, Album, user_artist, user_album, user_track
from src.functions import get_preview_url_if_null, token_required

main_bp = Blueprint('main', __name__)


@main_bp.before_request
def reset_session_tracks():
    if request.path != '/recommendations':
        if ('tracks' or 'genres_list') in session:
            del session['tracks']
            del session['genres_list']


@main_bp.route('/')
def home():
    if current_user.is_authenticated:
        current_user_tracks = current_user.tracks
    else:
        current_user_tracks = []
    tracks_data = db.session.query(user_track).all()
    recently_liked_tracks = [track for track in tracks_data]
    recently_liked_track_ids = [track[1] for track in recently_liked_tracks[-5:]]
    track_ids = {track[1] for track in recently_liked_tracks}
    tracks = Track.query.filter(Track.id.in_(recently_liked_track_ids)).all()
    liked_tracks_ids = {track.id for track in current_user_tracks}

    tracks_dict = {
        track.id: {'track': track, 'liked': track.id in liked_tracks_ids}
        for track in tracks
    }
    ordered_tracks = [tracks_dict[track_id] for track_id in reversed(recently_liked_track_ids)]

    tracks_for_genres = Track.query.filter(Track.id.in_(track_ids)).all()
    genres_like_count = Counter()
    for track in tracks_for_genres:
        genres = track.genres.split('.')
        genres_like_count.update(genres)
    popular_genres = {k:v for k, v in dict(genres_like_count.most_common()[:10]).items() if k}

    artists_data = db.session.query(user_artist).all()
    artist_ids = [artist[1] for artist in artists_data]
    artist_like_count = Counter(artist_ids)

    popular_artists = [artist_id for artist_id, _ in artist_like_count.most_common()]
    artists = Artist.query.filter(Artist.id.in_(popular_artists)).all()
    artist_dict = {artist.id: artist for artist in artists}

    artist_data_list = []
    for artist_id in popular_artists:
        artist = artist_dict[artist_id]
        artist_data_list.append({
            'id': artist_id,
            'name': artist.name,
            'image': artist.image,
        })

    albums_data = db.session.query(user_album).all()
    album_ids = [album[1] for album in albums_data]
    album_like_count = Counter(album_ids)

    popular_albums = [album_id for album_id, _ in album_like_count.most_common()]
    albums = Album.query.filter(Album.id.in_(popular_albums)).all()
    album_dict = {album.id: album for album in albums}

    album_data_list = []
    for album_id in popular_albums:
        album = album_dict[album_id]
        album_data_list.append({
            'id': album_id,
            'name': album.name,
            'cover': album.cover,
        })
    return render_template('main/home.html', recently_liked_tracks=ordered_tracks, artists=artists, albums=albums, genres=popular_genres)

@main_bp.route('/recommendations')
@login_required
@token_required
def recommendations():
    genres = {}
    seed_tracks = []
    for track in current_user.tracks:
        track_genres = str(track.genres).split('.')
        for genre in track_genres:
            if genre not in genres:
                genres[genre] = []
            genres[genre].append(track.id)
    if 'genres_list' not in session:
        session['genres_list'] = list(genres.keys())
    genres_list = session['genres_list']
    if not genres_list:
        genres_list = list(genres.keys())
    for _ in range(len(genres_list[:5])):
        random_genre = choice(genres_list)
        genre_songs = genres[random_genre]
        track_id = choice(genre_songs)
        seed_tracks.append(track_id)
        genres_list.remove(random_genre)
    session['genres_list'] = genres_list
    # janrebi
    # example_choice = ['art pop', 'jazz fusion', 'experimental']
    # for genre in example_choice:
    #     tracks = Track.query.filter(Track.genres.contains(genre)).all()
    #     for track in tracks:
    #         if genre not in genres:
    #             genres[genre] = []
    #         genres[genre].append(track.name)
    # for _ in range(len(example_choice)):
    #     random_genre = choice(example_choice)
    #     genre_songs = genres[random_genre]
    #     track_id = choice(genre_songs)
    #     seed_tracks.append(track_id)
    #     example_choice.remove(random_genre)
    # seed_tracks = ','.join(seed_tracks)
    # print(seed_tracks)
    # -------
    headers = {
        "Authorization": f"Bearer {session['access_token']}"
    }
    params = {
        'limit': 20,
        'market': 'US',
        'seed_tracks': seed_tracks,
    }

    response = requests.get(f'https://api.spotify.com/v1/recommendations?', headers=headers, params=params)
    if 'tracks' not in session:
        session['tracks'] = []
    tracks = []
    liked_tracks = {track.id for track in current_user.tracks}
    session_tracks = set(session['tracks'])
    for n in range(len(response.json()['tracks'])):
        track = response.json()['tracks'][n]
        track_id = track['id']
        if track_id not in liked_tracks and track_id not in session_tracks:
            track_body = {
                'name': track['name'].lower(),
                'id': track_id,
                'artists_name': '/'.join([artist['name'].lower() for artist in track['artists']]),
                'artists_id': ','.join([artist['id'] for artist in track['artists']]),
                'album_name': track['album']['name'].lower(),
                'album_id': track['album']['id'],
                'album_cover': track['album']['images'][0]['url'],
                'preview_url': track.get('preview_url') or get_preview_url_if_null(track_id),
            }
            tracks.append(track_body)
            session['tracks'].append(track_id)
    return render_template('main/recommendations.html', tracks=tracks)


@main_bp.route('/dlt')
def dlt():
    print(len(session['tracks']))
    del session['tracks']
    return ''
