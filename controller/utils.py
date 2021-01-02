from typing import *


def create_model_from_request(schema, request) -> Dict[str, Any]:
    item_properties = schema['properties'].keys()
    item = {}
    for prop in item_properties:
        if prop in request:
            item[prop] = request[prop]
    return item


def is_float(value) -> bool:
    try:
        float(value)
        return True
    except:
        return False
