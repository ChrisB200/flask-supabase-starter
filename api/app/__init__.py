import logging
import traceback
from flask import Flask, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_session import Session

from app.routes import routes
from app.config.config import ApplicationConfig
from app.config.logger import switch_logging_config, dev
from app.config.db import db
from app.utils.constants import ENVIRONMENT
from app.utils.exceptions import AppError


logging.config.dictConfig(dev)
logger = logging.getLogger(__name__)


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(ApplicationConfig)

    if test_config:
        app.config.update(test_config)

    CORS(
        app,
        supports_credentials=True,
        resources={r"/*": {"origins": "*"}}
    )

    Session(app)

    bcrypt = Bcrypt()
    bcrypt.init_app(app)

    db.init_app(app)

    app.register_blueprint(routes)

    # Custom app-level error (controlled)
    @app.errorhandler(AppError)
    def handle_app_error(e):
        logger.warning(f"AppError: {e.message}")
        return jsonify(error=e.message), e.status_code

    # Catch-all unhandled exception (500)
    @app.errorhandler(Exception)
    def handle_exception(e):
        trace = traceback.format_exc()
        logger.error(f"Unhandled Exception: {str(e)}\n{trace}")
        return jsonify(error="Internal Server Error"), 500

    return app
