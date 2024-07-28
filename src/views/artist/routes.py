import requests
from time import time
from flask import render_template, session, request, Blueprint, jsonify
from flask_login import login_required, current_user
from sqlalchemy import delete, exists

from src.extensions import cache, db
from src.models.models import Artist, user_artist
from src.functions import token_required


artist_bp = Blueprint('artist', __name__)


artists_list = [{'name': 'frank ocean', 'id': '2h93pZq0e7k5yf4dywlkpM',
                 'image': 'https://i.scdn.co/image/ab6761610000e5ebee3123e593174208f9754fab',
                 'genres': ['lgbtq+ hip hop', 'neo soul'],
                 'url': 'https://open.spotify.com/artist/2h93pZq0e7k5yf4dywlkpM'},
                {'name': 'frank sinatra', 'id': '1Mxqyy3pSjf8kZZL4QVxS0',
                 'image': 'https://i.scdn.co/image/fc4e0f474fb4c4cb83617aa884dc9fd9822d4411',
                 'genres': ['adult standards', 'easy listening', 'lounge'],
                 'url': 'https://open.spotify.com/artist/1Mxqyy3pSjf8kZZL4QVxS0'},
                {'name': 'frank zappa', 'id': '6ra4GIOgCZQZMOaUECftGN',
                 'image': 'https://i.scdn.co/image/e1c04d8144371d6a6ac39c7f15a1c2a9f67a0c50',
                 'genres': ['art rock', 'blues rock', 'experimental', 'instrumental rock', 'jazz fusion', 'jazz rock',
                            'progressive rock', 'psychedelic rock', 'symphonic rock', 'zolo'],
                 'url': 'https://open.spotify.com/artist/6ra4GIOgCZQZMOaUECftGN'},
                {'name': 'forrest frank', 'id': '1scVfBymTr3CeZ4imMj1QJ',
                 'image': 'https://i.scdn.co/image/ab6761610000e5eb51e72def9cfa6358ca2e08dc', 'genres': [],
                 'url': 'https://open.spotify.com/artist/1scVfBymTr3CeZ4imMj1QJ'},
                {'name': 'frankie valli & the four seasons', 'id': '6mcrZQmgzFGRWf7C0SObou',
                 'image': 'https://i.scdn.co/image/ab6761610000e5ebb327bc619c6db2f9dce5f431',
                 'genres': ['adult standards', 'bubblegum pop', 'doo-wop', 'lounge', 'northern soul', 'rock-and-roll',
                            'rockabilly'], 'url': 'https://open.spotify.com/artist/6mcrZQmgzFGRWf7C0SObou'},
                {'name': 'aretha franklin', 'id': '7nwUJBm0HE4ZxD3f5cy5ok',
                 'image': 'https://i.scdn.co/image/ab6761610000e5ebf12270128127ba170f90097d',
                 'genres': ['classic soul', 'jazz blues', 'memphis soul', 'soul', 'southern soul', 'vocal jazz'],
                 'url': 'https://open.spotify.com/artist/7nwUJBm0HE4ZxD3f5cy5ok'},
                {'name': 'frank turner', 'id': '27M9shmwhIjRo7WntpT9Rp',
                 'image': 'https://i.scdn.co/image/ab6761610000e5eb15bc846cba5e7daed061cb0c',
                 'genres': ['acoustic rock', 'folk punk', 'scottish rock'],
                 'url': 'https://open.spotify.com/artist/27M9shmwhIjRo7WntpT9Rp'},
                {'name': 'frankie ruiz', 'id': '4dLvccxeQIM5u80Ri0u9OV',
                 'image': 'https://i.scdn.co/image/ab67616d0000b2731090772b21a561bfa6d71f86',
                 'genres': ['salsa', 'salsa puertorriquena', 'tropical'],
                 'url': 'https://open.spotify.com/artist/4dLvccxeQIM5u80Ri0u9OV'},
                {'name': 'kirk franklin', 'id': '4akybxRTGHJZ1DXjLhJ1qu',
                 'image': 'https://i.scdn.co/image/ab6761610000e5ebd0a257c74c32388d98386f6b',
                 'genres': ['gospel', 'gospel r&b'], 'url': 'https://open.spotify.com/artist/4akybxRTGHJZ1DXjLhJ1qu'},
                {'name': 'frankie valli', 'id': '3CDKmzJu6uwEGnPLLZffpD',
                 'image': 'https://i.scdn.co/image/ab6772690000c46cb8af37ba12c1ad7ebcc63c25',
                 'genres': ['adult standards', 'bubblegum pop', 'lounge', 'rock-and-roll'],
                 'url': 'https://open.spotify.com/artist/3CDKmzJu6uwEGnPLLZffpD'},
                {'name': 'frankie j', 'id': '3sMYEBy0CZFxedcnm9i9hf',
                 'image': 'https://i.scdn.co/image/ab6761610000e5eb7d6cf53c9feae4bd97688990',
                 'genres': ['hip pop', 'pop rap', 'southern hip hop', 'urban contemporary'],
                 'url': 'https://open.spotify.com/artist/3sMYEBy0CZFxedcnm9i9hf'},
                {'name': 'frank reyes', 'id': '4vQV1LCGBdYAt5rIIPjSFZ',
                 'image': 'https://i.scdn.co/image/ab6761610000e5ebbbe87779d198b31d6d54b80c',
                 'genres': ['bachata', 'bachata dominicana'],
                 'url': 'https://open.spotify.com/artist/4vQV1LCGBdYAt5rIIPjSFZ'},
                {'name': 'frank foster', 'id': '77GSkIzDaduRlIbNjlvefc',
                 'image': 'https://i.scdn.co/image/ab6761610000e5ebe909ba04b519c0235cb8148a', 'genres': [],
                 'url': 'https://open.spotify.com/artist/77GSkIzDaduRlIbNjlvefc'},
                {'name': 'frankie ballard', 'id': '0dvKgSdNB2U1gfp6ZcekYi',
                 'image': 'https://i.scdn.co/image/ab6761610000e5eb3b1dff850d167adf76109b3a',
                 'genres': ['contemporary country', 'country road', 'modern country rock'],
                 'url': 'https://open.spotify.com/artist/0dvKgSdNB2U1gfp6ZcekYi'},
                {'name': 'frankie goes to hollywood', 'id': '1mZu3rO7qSD09GdDpePHhY',
                 'image': 'https://i.scdn.co/image/ab6761610000e5ebe7efd9cceef0829d1439b11e',
                 'genres': ['dance rock', 'hi-nrg', 'new romantic', 'new wave', 'new wave pop', 'synthpop'],
                 'url': 'https://open.spotify.com/artist/1mZu3rO7qSD09GdDpePHhY'},
                {'name': 'frankie cosmos', 'id': '0x4xCoWaOFd3WsKarzaxnW',
                 'image': 'https://i.scdn.co/image/ab6761610000e5eb1cf8d6f0ed6dbcc294852ddc',
                 'genres': ['bedroom pop', 'bubblegrunge', 'indie pop'],
                 'url': 'https://open.spotify.com/artist/0x4xCoWaOFd3WsKarzaxnW'},
                {'name': 'frank walker', 'id': '6rcE30MaP92XafelMNZ2Sq',
                 'image': 'https://i.scdn.co/image/ab6761610000e5eb7e075b089fe926b21e03e85f', 'genres': [],
                 'url': 'https://open.spotify.com/artist/6rcE30MaP92XafelMNZ2Sq'},
                {'name': 'frank', 'id': '1c1zan5bb0iXtzLDHrptRe',
                 'image': 'https://i.scdn.co/image/ab6761610000e5eb57b08a8da9cfb1fd1474c071', 'genres': [],
                 'url': 'https://open.spotify.com/artist/1c1zan5bb0iXtzLDHrptRe'},
                {'name': 'frankie beverly', 'id': '6rXycobs8wkWicUGLtmB0n',
                 'image': 'https://i.scdn.co/image/f0351adb45404fc8ca9cc399a70e32f62db5e021', 'genres': ['quiet storm'],
                 'url': 'https://open.spotify.com/artist/6rXycobs8wkWicUGLtmB0n'},
                {'name': 'frank', 'id': '2q1lPSowgmgiCLtnSRMNMD',
                 'image': 'https://i.scdn.co/image/ab67616d0000b273212d18799a2f7ceafd39a65f', 'genres': [],
                 'url': 'https://open.spotify.com/artist/2q1lPSowgmgiCLtnSRMNMD'}]


@artist_bp.route('/search')
@login_required
@token_required
def search_artist():
    artist_name = request.args.get('search_query')
    artists = []
    headers = {
        "Authorization": f"Bearer {session['access_token']}"
    }

    response_search = requests.get(f'https://api.spotify.com/v1/search?q={artist_name}&type=artist', headers=headers)

    for artist in response_search.json()['artists']['items']:
        check = exists().where(
            db.and_(
                user_artist.c.user_id == current_user.id,
                user_artist.c.artist_id == artist['id']
            )
        )
        result = db.session.query(check).scalar()
        if artist['images']:
            artist_image_url = artist['images'][0]['url']
            if not any(existing_artist['image'] == artist_image_url for existing_artist in artists):
                artist_body = {
                    'name': artist['name'].lower(),
                    'id': artist['id'],
                    'image': artist_image_url,
                    'genres': artist['genres'],
                    'url': artist['external_urls']['spotify']
                }
                artist_body['followed'] = result
                artists.append(artist_body)


    return render_template('artist/search.html', artists=artists, title=artist_name)


@artist_bp.route('/artist/<id>')
@login_required
@token_required
# @cache.cached(timeout=120)
def artist(id):
    albums = []
    headers = {
        "Authorization": f"Bearer {session['access_token']}"
    }
    params = {
        'limit': 50,
        'include_groups': 'album,single'
    }
    response_album = requests.get(f'https://api.spotify.com/v1/artists/{id}/albums', headers=headers, params=params)
    response_artist = requests.get(f'https://api.spotify.com/v1/artists/{id}', headers=headers)

    artist_body = {
        'name': response_artist.json()['name'].lower(),
        'id': response_artist.json()['id'],
        'genres': response_artist.json()['genres'],
        'image': response_artist.json()['images'][0]['url'],
        'url': response_artist.json()['external_urls']['spotify']
    }

    for album in response_album.json()['items']:
        album_body = {
            'name': album['name'].lower(),
            'id': album['id'],
            'cover': album['images'][0]['url'],
            'release_date': album['release_date'],
            'artists': [artist['name'].lower() for artist in album['artists']],
            'type': album['album_group'],
            'url': album['external_urls']['spotify']
        }
        albums.append(album_body)


    return render_template('artist/artist_page.html', albums=albums, artist=artist_body)


@artist_bp.route('/artist/<id>/singles')
@login_required
@token_required
@cache.cached(timeout=120)
def artist_singles(id):
    singles = []
    headers = {
        "Authorization": f"Bearer {session['access_token']}"
    }
    params = {
        'limit': 50,
        'include_groups': 'single'
    }
    response_single = requests.get(f'https://api.spotify.com/v1/artists/{id}/albums', headers=headers, params=params)


    for single in response_single.json()['items']:
        single_body = {
            'name': single['name'].lower(),
            'id': single['id'],
            'cover': single['images'][0]['url'],
            'release_date': single['release_date'],
            'artists': [artist['name'].lower() for artist in single['artists']],
            'type': single['album_group'],
            'url': single['external_urls']['spotify']
        }
        singles.append(single_body)
    return jsonify(singles)


@artist_bp.route('/artist/<id>/albums')
@login_required
@token_required
@cache.cached(timeout=120)
def artist_albums(id):
    albums = []
    headers = {
        "Authorization": f"Bearer {session['access_token']}"
    }
    params = {
        'limit': 50,
        'include_groups': 'album'
    }
    response_album = requests.get(f'https://api.spotify.com/v1/artists/{id}/albums', headers=headers, params=params)


    for album in response_album.json()['items']:
        album_body = {
            'name': album['name'].lower(),
            'id': album['id'],
            'cover': album['images'][0]['url'],
            'release_date': album['release_date'],
            'artists': [artist['name'].lower() for artist in album['artists']],
            'type': album['album_group'],
            'url': album['external_urls']['spotify']
        }
        albums.append(album_body)
    return jsonify(albums)


@artist_bp.route('/follow-artist/<id>', methods=['POST'])
@login_required
def follow_artist(id):
    name = request.form.get('name')
    image = request.form.get('image')
    genres = request.form.get('genres')
    artist = Artist.query.filter_by(id=id).first()
    if not artist:
        artist = Artist(id=id, name=name, image=image, genres=genres)
        artist.create()
    if artist not in current_user.artists:
        current_user.artists.append(artist)
        current_user.save()
        return jsonify({'message': 'You followed the artist.'})
    return jsonify({'message': 'You are already following the artist.'})


@artist_bp.route('/unfollow-artist/<id>', methods=['POST'])
@login_required
def unfollow_artist(id):
    delete_stmt = delete(user_artist).where(
        db.and_(
            user_artist.c.user_id == current_user.id,
            user_artist.c.artist_id == id
        )
    )
    artist = Artist.query.filter_by(id=id).first()
    if artist:
        artist.delete()
        db.session.execute(delete_stmt)
        db.session.commit()
        return jsonify({'message': 'You unfollowed artist.'})
    return jsonify({'message': "You aren't following the artist."})