from typing import *

from bson import json_util
from flask import json


def create_model_from_request(schema, request) -> Dict[str, Any]:
    item_properties = schema['properties'].keys()
    item = {}
    for prop in item_properties:
        if prop in request:
            item[prop] = request[prop]
    return item


def parse_json(data):
    return json.loads(json_util.dumps(data))
