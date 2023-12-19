from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from app.models.user import User
from app.models import storage
from app.main.main import main
from app.auth.auth import auth
"""Entry point
"""


app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasecret'
login_manager = LoginManager()
login_manager.init_app(app)
cors = CORS(app)
app.register_blueprint(main)
app.register_blueprint(auth)

@login_manager.user_loader
def user_loader(user_id):
    """Given 'user_id', returns associated
    User object
    """
    return User.query.get(int(user_id))



if __name__ == "__main__":
    app.run(debug=True)