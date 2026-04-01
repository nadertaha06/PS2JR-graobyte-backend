from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    origens = app.config.get('CORS_ORIGINS', '*')
    CORS(app, origins=origens)
    JWTManager(app)

    from app.routes.auth import auth_bp
    # from app.routes.produtos import produtos_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    # app.register_blueprint(produtos_bp, url_prefix='/produtos')

    return app
