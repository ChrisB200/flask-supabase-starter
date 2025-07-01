from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from datetime import timezone
from datetime import datetime

import math

db = SQLAlchemy()


def get_uuid():
    return uuid4().hex


def get_timestamp(tz=timezone.utc):
    now = datetime.now(tz)
    timestamp = now.replace(tzinfo=tz).timestamp()
    return math.floor(timestamp)
