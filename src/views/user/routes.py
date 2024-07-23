from flask import Blueprint, session, render_template, jsonify
from flask_login import current_user, login_required
from sqlalchemy import exists
from collections import Counter

from src.models.models import User, Artist, Album, Track, user_artist, user_album, user_track, followers
from src.extensions import db
from src.functions import token_required


user_bp = Blueprint('user', __name__)


@user_bp.route('/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first()
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
    return render_template('user/profile.html', id=user.id, username=username, genres=favorite_genres, tracks=reversed(recently_liked_tracks[-4:]), artists=reversed(recently_liked_artists[-4:]))


@user_bp.route('/follow-user/<int:id>')
@login_required
def follow_user(id):
    user = User.query.filter_by(id=current_user.id).first()
    user_to_follow = User.query.filter_by(id=id).first()
    if not user.is_following(user_to_follow):
        user.follow(user_to_follow)
        db.session.commit()
        return jsonify({'message': 'You followed the user.'})
    return jsonify({'message': 'You are already following the user.'})


@user_bp.route('/unfollow-user/<int:id>')
@login_required
def unfollow_user(id):
    user = User.query.filter_by(id=current_user.id).first()
    user_to_unfollow = User.query.filter_by(id=id).first()
    if user.is_following(user_to_unfollow):
        user.unfollow(user_to_unfollow)
        db.session.commit()
        return jsonify({'message': 'You unfollowed the user.'})
    return jsonify({'message': "You aren't following the user."})


@user_bp.route('/<username>/liked-tracks/')
def liked_tracks(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message': "User doesn't exists."})
    return ''