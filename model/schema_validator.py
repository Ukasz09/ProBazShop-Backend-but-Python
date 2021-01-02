from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema
from model.schema import *
from typing import List, Type, Optional


class ItemValidator(Inputs):
    json = [JsonSchema(schema=item_schema)]


class UserValidator(Inputs):
    json = [JsonSchema(schema=user_schema)]


def validate_data(request, validator: Type[Inputs]) -> Optional[List]:
    inputs = validator(request)
    if inputs.validate():
        return None
    else:
        return inputs.errors
