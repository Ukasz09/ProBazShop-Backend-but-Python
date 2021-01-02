from flask import jsonify, request
from flask_cors import cross_origin
from app import app
from controller import item_controller
from model import schema_validator
from controller.error_handler import InvalidUsage


@app.route('/api/items', methods=['GET', 'POST', 'DELETE'])
@cross_origin()
def items():
    try:
        if request.method == 'POST':
            errors = schema_validator.validate_data(request, schema_validator.ItemValidator)
            if errors is not None:
                raise InvalidUsage(errors)
            return jsonify(item_controller.create(request.json))
        elif request.method == 'GET':
            return jsonify(item_controller.find_all(request.args))
        else:
            return jsonify(item_controller.delete_all())
    except InvalidUsage as e:
        raise e
    except Exception as e:
        raise InvalidUsage('Database connection error', 500)


@app.route('/api/items/<item_id>', methods=['GET', 'PUT', 'DELETE'])
@cross_origin()
def item_by_id(item_id: str):
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


@app.route('/api/categories', methods=['GET'])
@cross_origin()
def categories():
    return jsonify(item_controller.get_categories())
