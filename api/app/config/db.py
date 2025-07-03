from flask_sqlalchemy import SQLAlchemy
from datetime import timezone
from datetime import datetime

import math

db = SQLAlchemy()


def get_timestamp(tz=timezone.utc):
    now = datetime.now(tz)
    timestamp = now.replace(tzinfo=tz).timestamp()
    return math.floor(timestamp)
