import pymongo

import dbconn
from model.schema import *
from controller.utils import *
from bson.objectid import ObjectId


def create(request: Dict[str, Any]) -> Optional[Dict[str, str]]:
    item = create_model_from_request(item_schema, request)
    result = dbconn.items_collection.insert_one(item)
    del item['_id']
    item['id'] = str(result.inserted_id)
    return item


def find_all(query_args: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
    db_query, sort_param, sort_direction = _parse_find_query(query_args)
    result = []
    result += dbconn.items_collection.find(db_query).sort(sort_param, sort_direction)
    for item in result:
        item['id'] = str(item['_id'])
        del item['_id']
    return result


def _parse_find_query(query_args: Dict[str, Any]) -> (Dict[str, Any], str, int):
    db_query = {}

    if 'name' in query_args:
        db_query['name'] = {'$regex': query_args['name'], '$options': 'i'}

    if 'category' in query_args:
        categories = query_args['category'].split(',')
        db_query['category'] = {'$in': categories}

    if 'size' in query_args:
        sizes = query_args['size'].split(',')
        db_query['size'] = {'$in': sizes}

    if 'price_from' in query_args and 'price_to' in query_args:
        if is_float(query_args['price_from']) and is_float(query_args['price_to']):
            price_from = float(query_args['price_from'])
            price_to = float(query_args['price_to'])
            db_query['price'] = {'$gte': price_from, '$lte': price_to}
    elif 'price_from' in query_args and is_float(query_args['price_from']):
        price_from = float(query_args['price_from'])
        db_query['price'] = {'$gte': price_from}
    elif 'price_to' in query_args and is_float(query_args['price_to']):
        price_to = float(query_args['price_to'])
        db_query['price'] = {'$lte': price_to}

    if 'color' in query_args:
        colors = query_args['color'].split(',')
        colors_with_hash = []
        for color in colors:
            colors_with_hash.append('#{color}'.format(color=color))
        db_query['color'] = {'$in': colors_with_hash}

    if 'starRating' in query_args:
        db_query['starRating'] = {'$gt': query_args['starRating']}
    sort_param = 'createdAt'
    sort_direction = pymongo.DESCENDING
    if 'sort' in query_args:
        sort_direction = pymongo.ASCENDING if query_args['sort'] == 'asc' else pymongo.DESCENDING
        sort_param = 'price'
    print(db_query)
    return db_query, sort_param, sort_direction


def delete_all() -> Optional[Dict[str, str]]:
    result = dbconn.items_collection.delete_many({})
    return {'message': 'Deleted count: {count}'.format(count=result.deleted_count)}


def find(item_id: str):
    try:
        id = ObjectId(item_id)
    except Exception:
        return None
    cursor = dbconn.items_collection.find({'_id': id})
    result = list(cursor)
    if len(result) == 0:
        return None
    item = result[0]
    item['id'] = item_id
    del item['_id']
    return item


def update(item_id: str, request: Dict[str, Any]):
    item = create_model_from_request(item_schema, request)
    try:
        id = ObjectId(item_id)
    except Exception:
        return None
    result = dbconn.items_collection.find_one_and_update(
        {"_id": id},
        {"$set": item},
        upsert=False
    )
    if result is None:
        return result
    result['id'] = item_id
    del result['_id']
    return result


def delete(item_id: str):
    try:
        id = ObjectId(item_id)
    except Exception:
        return None
    result = dbconn.items_collection.find_one_and_delete({'_id': id})
    if result is None:
        return result
    result['id'] = item_id
    del result['_id']
    return result


def get_categories():
    categories = dbconn.items_collection.find({}).distinct("category")
    return categories
