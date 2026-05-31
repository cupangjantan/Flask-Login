from flask import Flask
from routes.auth import auth
from routes.dashboard import dash 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard-to-guess-string-12345!@#$%'

app.register_blueprint(auth)
app.register_blueprint(dash)

if __name__ == "__main__":
    app.run(debug=True)