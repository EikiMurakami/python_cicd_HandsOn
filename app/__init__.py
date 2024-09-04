from flask import Flask
from .models import db
from .routes import bp as main_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
    app.config['SECRET_KEY'] = 'dev'

    db.init_app(app)
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    return app
