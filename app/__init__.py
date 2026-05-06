from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import secrets

db = SQLAlchemy()
jwt_secret = secrets.token_hex(32)

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/challenge.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = secrets.token_hex(32)
    
    db.init_app(app)
    
    from .limiter import limiter
    limiter.init_app(app)
    
    from .routes import bp, init_admin_user
    app.register_blueprint(bp)
    
    with app.app_context():
        db.create_all()
        init_admin_user()
    
    return app
