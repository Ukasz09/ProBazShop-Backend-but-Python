import dbconn
from model.schema import *
from controller.utils import *
from bson.objectid import ObjectId


# TODO: avoid adding with the same email
def create(request: Dict[str, Any]) -> Optional[Dict[str, str]]:
    user = create_model_from_request(user_schema, request)
    result = dbconn.users_collection.insert_one(user)
    del user['_id']
    user['id'] = str(result.inserted_id)
    return user


def find_all(query_args: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
    db_query = {}
    if 'name' in query_args:
        db_query['name'] = {'$regex': query_args['name'], '$options': 'i'}
    result = []
    result += dbconn.users_collection.find(db_query)
    for item in result:
        item['id'] = str(item['_id'])
        del item['_id']
    return result
