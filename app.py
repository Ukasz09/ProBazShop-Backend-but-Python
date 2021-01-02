from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
from routes import item_routes
from routes import user_routes

# TODO: remove redundancy in user / item controllers
# TODO: avoid adding with the same email
if __name__ == '__main__':
    app.run(debug=True)
