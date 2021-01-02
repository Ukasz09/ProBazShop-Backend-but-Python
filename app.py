from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
from routes import item_routes
from routes import user_routes

# TODO: add typing
# TODO: remove redundancy in user / item controllers
# TODO: rename routes to provide compatibility with frontend
if __name__ == '__main__':
    app.run(debug=True)
