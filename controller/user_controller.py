import dbconn
from model.schema import *
from controller.utils import *
from bson.objectid import ObjectId


def create(request: Dict[str, Any]) -> Optional[Dict[str, str]]:
    user = create_model_from_request(user_schema, request)
    result = dbconn.users_collection.insert_one(user)
    del user['_id']
    user['id'] = str(result.inserted_id)
    return user
