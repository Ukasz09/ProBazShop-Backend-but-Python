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


def delete_all() -> Optional[Dict[str, str]]:
    result = dbconn.users_collection.delete_many({})
    return {'message': 'Deleted count: {count}'.format(count=result.deleted_count)}


def find(user_id: str) -> Optional[Dict[str, Any]]:
    try:
        id = ObjectId(user_id)
    except Exception:
        return None
    cursor = dbconn.users_collection.find({'_id': id})
    result = list(cursor)
    if len(result) == 0:
        return None
    item = result[0]
    item['id'] = user_id
    del item['_id']
    return item


def update(user_id: str, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    user = create_model_from_request(user_schema, request)
    try:
        id = ObjectId(user_id)
    except Exception:
        return None
    result = dbconn.users_collection.find_one_and_update(
        {"_id": id},
        {"$set": user},
        upsert=False
    )
    if result is None:
        return result
    result['id'] = user_id
    del result['_id']
    return result


def delete(user_id: str) -> Optional[Dict[str, Any]]:
    try:
        id = ObjectId(user_id)
    except Exception:
        return None
    result = dbconn.users_collection.find_one_and_delete({'_id': id})
    if result is None:
        return result
    result['id'] = user_id
    del result['_id']
    return result


def get_history(user_id) -> Optional[List[Dict[str, Any]]]:
    try:
        id = ObjectId(user_id)
    except Exception:
        return None
    cursor = dbconn.users_collection.find({'_id': id})
    result = list(cursor)
    if len(result) == 0:
        return None
    user = result[0]
    if 'history' in user:
        return user['history']
    else:
        return []


def login(email: str, password: str) -> Optional[Dict[str, Any]]:
    cursor = dbconn.users_collection.find({'email': email, 'password': password})
    result = list(cursor)
    if len(result) == 0:
        return None
    user = result[0]
    user['id'] = str(user['_id'])
    del user['_id']
    return user
