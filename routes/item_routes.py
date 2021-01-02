from flask import jsonify, request
from flask_cors import cross_origin
from app import app
from controller import item_controller
from model import schema_validator


@app.route('/items', methods=['GET', 'POST', 'DELETE'])
@cross_origin()
def items():
    if request.method == 'POST':
        errors = schema_validator.validate_greeting(request, schema_validator.ItemValidator)
        if errors is not None:
            raise InvalidUsage(errors)
        result = item_controller.create(request.json)
        return _return_with_db_conn_validation(result)
    elif request.method == 'GET':
        result = item_controller.find_all(request.args)
        return _return_with_db_conn_validation(result)
    else:
        result = item_controller.delete_all()
        return _return_with_db_conn_validation(result)


@app.route('/items/<item_id>', methods=['GET', 'PUT'])
@cross_origin()
def item_by_id(item_id: int):
    if request.method == 'GET':
        result = item_controller.find(item_id)
        if result:
            return jsonify(result)
        else:
            return {"message": "Not found item with given ID"}, 404
    elif request.method == 'PUT':
        return jsonify(item_controller.update(item_id))
    else:
        return jsonify(item_controller.delete(item_id))


@app.route('/api/categories', methods=['GET'])
@cross_origin()
def categories():
    return jsonify(item_controller.get_categories())


########################################################################################################################
class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def _return_with_db_conn_validation(result):
    if result is None:
        raise InvalidUsage('Database connection error', 500)
    return jsonify(result)
