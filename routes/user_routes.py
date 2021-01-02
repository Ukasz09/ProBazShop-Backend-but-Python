from flask import jsonify, request
from flask_cors import cross_origin
from app import app
from controller import user_controller
from model import schema_validator
from routes.item_routes import InvalidUsage


@app.route('/users', methods=['GET', 'POST', 'DELETE'])
@cross_origin()
def users():
    try:
        if request.method == 'POST':
            errors = schema_validator.validate_data(request, schema_validator.UserValidator)
            if errors is not None:
                raise InvalidUsage(errors)
            return jsonify(user_controller.create(request.json))
        elif request.method == 'GET':
            return jsonify(user_controller.find_all(request.args))
        else:
            return jsonify(item_controller.delete_all())
    except InvalidUsage as e:
        raise e
    except Exception as e:
        raise InvalidUsage('Database connection error', 500)


@app.route('/user/<user_id>', methods=['GET', 'PUT', 'DELETE'])
@cross_origin()
def user_by_id(item_id: str):
    try:
        if request.method == 'GET':
            result = item_controller.find(item_id)
            if result:
                return jsonify(result)
            else:
                return {"message": "Not found item with given ID"}, 404
        elif request.method == 'PUT':
            errors = schema_validator.validate_data(request, schema_validator.ItemValidator)
            if errors is not None:
                raise InvalidUsage(errors)
            result = item_controller.update(item_id, request.json)
            if result:
                return jsonify(result)
            else:
                return {"message": "Not found item with given ID"}, 404
        else:
            result = item_controller.delete(item_id)
            if result:
                return jsonify(result)
            else:
                return {"message": "Not found item with given ID"}, 404
    except InvalidUsage as e:
        raise e
    except Exception as e:
        raise InvalidUsage('Database connection error', 500)


@app.route('/history/<user_id>', methods=['GET'])
@cross_origin()
def history(user_id: str):
    pass


@app.route('/login', methods=['GET'])
@cross_origin()
def logon():
    pass
