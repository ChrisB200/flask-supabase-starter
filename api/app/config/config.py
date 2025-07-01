# from redis import Redis

from app.utils.constants import SECRET_KEY, DB_URL


class ApplicationConfig:
    SECRET_KEY = SECRET_KEY

    # ----- SESSION -----
    # redis
    # SESSION_TYPE = "redis"
    # SESSION_REDIS = Redis.from_url(REDIS_URL)
    # SESSION_PERMANENT = False
    # SESSION_USE_SIGNER = True

    # filesystem
    SESSION_TYPE = "filesystem"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True

    # ----- SQLALCHEMY -----
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = DB_URL
