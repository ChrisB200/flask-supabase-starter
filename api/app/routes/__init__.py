from flask import Blueprint
from app.routes.auth import auth_bp
from app.routes.account import account_bp

routes = Blueprint("routes", __name__)

routes.register_blueprint(auth_bp, url_prefix="/auth")
routes.register_blueprint(account_bp, url_prefix="/accounts")
