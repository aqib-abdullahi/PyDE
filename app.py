from flask import Flask
from flask_cors import CORS
from app.main.main import main
"""Entry point
"""


app = Flask(__name__)
cors = CORS(app)
app.register_blueprint(main)


if __name__ == "__main__":
    app.run(debug=True)