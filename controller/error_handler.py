from flask import jsonify

from app import app


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, description, code=None, payload=None):
        Exception.__init__(self)
        self.description = description
        if code is not None:
            self.status_code = code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.description
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
