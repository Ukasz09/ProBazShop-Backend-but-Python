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
            return jsonify(user_controller.delete_all())
    except InvalidUsage as e:
        raise e
    except Exception as e:
        raise InvalidUsage('Database connection error', 500)


@app.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
@cross_origin()
def user_by_id(user_id: str):
    try:
        if request.method == 'GET':
            result = user_controller.find(user_id)
            if result:
                return jsonify(result)
            else:
                return {"message": "Not found user with given ID"}, 404
        elif request.method == 'PUT':
            errors = schema_validator.validate_data(request, schema_validator.UserValidator)
            if errors is not None:
                raise InvalidUsage(errors)
            result = user_controller.update(user_id, request.json)
            if result:
                return jsonify(result)
            else:
                return {"message": "Not found user with given ID"}, 404
        else:
            result = user_controller.delete(user_id)
            if result:
                return jsonify(result)
            else:
                return {"message": "Not found user with given ID"}, 404
    except InvalidUsage as e:
        raise e
    except Exception as e:
        raise InvalidUsage('Database connection error', 500)


# TODO: implement
@app.route('/history/<user_id>', methods=['GET'])
@cross_origin()
def history(user_id: str):
    pass


# TODO: implement
@app.route('/login', methods=['GET'])
@cross_origin()
def logon():
    pass
