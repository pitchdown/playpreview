from redis import Redis


class Config:
    SECRET_KEY = 'secret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    CLIENT_ID = ''
    CLIENT_SECRET = ''
    LASTFM_KEY = ''
    REDIRECT_URI = ''
    AUTH_URL = 'https://accounts.spotify.com/authorize'
    TOKEN_URL = 'https://accounts.spotify.com/api/token'
    CACHE_TYPE = 'SimpleCache'
    SESSION_TYPE = 'redis'
    SESSION_REDIS = Redis(host='localhost', port=6379, db=0)