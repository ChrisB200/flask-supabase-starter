import os
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv(verbose=True, override=True)


def get_env(key, fallback=None):
    env_variable = os.getenv(key)
    if env_variable:
        return env_variable

    if not fallback:
        raise KeyError(f"Missing environment variable: {key}")

    logger.debug(f"Using fallback environment variable for key: {key}")

    return fallback


# DEFINE ENVIRONMENT VARIABLES HERE
SECRET_KEY = get_env("SECRET_KEY")
ENVIRONMENT = get_env("ENVIRONMENT", "dev")
FRONTEND_URL = get_env("FRONTEND_URL", "http://127.0.0.1:5173")

# ----- MYSQL -----
# INSTALL - poetry add pymysql

# DB_USERNAME = get_env("DB_USERNAME")
# DB_PASSWORD = get_env("DB_PASSWORD")
# DB_HOST = get_env("DB_HOST")
# DB_DATABASE = get_env("DB_DATABASE")
# DB_PORT = get_env("DB_PORT", 3306)
# DB_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"

# ----- POSTGRES -----
# INSTALL - poetry add psycopg2-binary

DB_USERNAME = get_env("DB_USERNAME")
DB_PASSWORD = get_env("DB_PASSWORD")
DB_HOST = get_env("DB_HOST")
DB_DATABASE = get_env("DB_DATABASE")
DB_PORT = get_env("DB_PORT", 5432)
DB_URL = f"postgresql://{DB_USERNAME}:{
    DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"

# ----- SQLITE -----
# DB_URL = "sqlite:///<path>"
# DB_URL = "sqlite:///:memory:"

# REDIS SETUP UNCOMMENT IF USING
# INSTALL - poetry add redis
# REDIS_URL = get_env("REDIS_URL")

# ----- SUPABASE -----
SUPABASE_API_URL = get_env("SUPABASE_API_URL")
SUPABASE_ANON_KEY = get_env("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_KEY = get_env("SUPABASE_SERVICE_KEY")
