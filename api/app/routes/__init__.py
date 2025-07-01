from flask import Blueprint
from app.routes.auth import auth_bp

routes = Blueprint("routes", __name__)

routes.register_blueprint(auth_bp, url_prefix="/auth")
