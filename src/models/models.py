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


followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
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

    following = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    def follow(self, user):
        if not self.is_following(user):
            self.following.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)

    def is_following(self, user):
        return self.following.filter(
            followers.c.followed_id == user.id).count() > 0

    def is_followed_by(self, user):
        return self.followers.filter(
            followers.c.follower_id == user.id).count() > 0


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

