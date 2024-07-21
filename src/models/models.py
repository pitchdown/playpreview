from src.extensions import db
from src.models.base import Base
from flask_login import UserMixin
from datetime import datetime


user_track = db.Table(
    'user_track',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('track_id', db.String, db.ForeignKey('track.id')),
)


user_artist = db.Table(
    'user_artist',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('artist_id', db.String, db.ForeignKey('artist.id')),
    db.Column('favorited', db.Boolean, default=False),
    db.Column('order', db.Integer)
)


user_album = db.Table(
    'user_album',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('album_id', db.String, db.ForeignKey('album.id')),
    db.Column('favorited', db.Boolean, default=False),
    db.Column('order', db.Integer)
)


class User(Base, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    role = db.Column(db.String)

    tracks = db.relationship('Track', secondary=user_track, back_populates='users')
    artists = db.relationship('Artist', secondary=user_artist, back_populates='users')
    albums = db.relationship('Album', secondary=user_album, back_populates='users')


class Track(Base):
    __tablename__ = 'track'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    artist_name = db.Column(db.String)
    artist_id = db.Column(db.String)
    album_name = db.Column(db.String)
    album_id = db.Column(db.String)
    album_cover = db.Column(db.String)
    preview_url = db.Column(db.String)
    genres = db.Column(db.String)

    users = db.relationship('User', secondary=user_track, back_populates='tracks')


class Artist(Base):
    __tablename__ = 'artist'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    image = db.Column(db.String)
    genres = db.Column(db.String)

    users = db.relationship('User', secondary=user_artist, back_populates='artists')


class Album(Base):
    __tablename__ = 'album'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    artist_id = db.Column(db.String)
    cover = db.Column(db.String)
    type = db.Column(db.String)
    total_tracks = db.Column(db.Integer)
    release_date = db.Column(db.String)

    users = db.relationship('User', secondary=user_album, back_populates='albums')

