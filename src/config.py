from redis import Redis


class Config:
    SECRET_KEY = 'secret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    CLIENT_ID = '6e82327445994df88d17de8cd6608f19'
    CLIENT_SECRET = 'e54f53e8cc4f46aab0b46d553c9bc022'
    LASTFM_KEY = 'ffb323dfd839f8050a2093b686654de7'
    REDIRECT_URI = 'http://localhost:5000/callback'
    AUTH_URL = 'https://accounts.spotify.com/authorize'
    TOKEN_URL = 'https://accounts.spotify.com/api/token'
    CACHE_TYPE = 'SimpleCache'
    SESSION_TYPE = 'redis'
    SESSION_REDIS = Redis(host='localhost', port=6379)