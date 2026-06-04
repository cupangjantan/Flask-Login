from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hard-to-guess-string-12345!@#$%'

    from app.routes.auth import auth
    from app.routes.dashboard import dash 
    app.register_blueprint(auth)
    app.register_blueprint(dash)

    return app
