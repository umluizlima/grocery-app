import os
from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__,
                instance_relative_config=True,
                static_url_path='')
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY') or 'you-will-never-guess',
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(app.instance_path, 'app.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    cors = CORS(app, resources={r"/list/*": {"origins": "*"}})

    from flask_sslify import SSLify
    if 'DYNO' in os.environ:
        sslify = SSLify(app)

    from app.model import db, ma, migrate
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    from app.controller import main, api
    app.register_blueprint(main.bp)
    app.register_blueprint(api.bp)

    return app
