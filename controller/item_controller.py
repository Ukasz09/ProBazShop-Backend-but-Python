import pymongo

import dbconn
from model.schema import *
from controller.utils import *


def create(request: Dict[str, Any]) -> Optional[Dict[str, str]]:
    item = create_model_from_request(item_schema, request)
    try:
        result = dbconn.items_collection.insert_one(item)
        del item['_id']
        item['id'] = str(result.inserted_id)
        return item
    except Exception as e:
        return None


def find_all(query_args: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
    try:
        db_query, sort_param, sort_direction = _parse_find_query(query_args)
        result = []
        result += dbconn.items_collection.find(db_query).sort(sort_param, sort_direction)
        for item in result:
            item['id'] = str(item['_id'])
            del item['_id']
        return result
    except Exception as e:
        return None


def _parse_find_query(query_args: Dict[str, Any]) -> (Dict[str, Any], str, int):
    db_query = {}

    if 'name' in query_args:
        db_query['name'] = {'$regex': query_args['name'], '$options': 'i'}

    if 'category' in query_args:
        categories = query_args['category'].split(',')
        db_query['category'] = {'$in': categories}

    if 'size' in query_args:
        sizes = query_args['size'].split(',')
        db_query['size'] = sizes

    if 'price_from' in query_args:
        if 'price_to' in query_args:
            db_query['price'] = {'$gt': query_args['price_from'], '$lt': query_args['price_to']}
        else:
            db_query['price'] = {'$gt': query_args['price_from']}
    elif 'price_to' in query_args:
        db_query['price'] = {'$lt': query_args['price_to']}

    if 'color' in query_args:
        colors = query_args['color'].split(',')
        colors_with_hash = []
        for color in colors:
            colors_with_hash.append('#{color}'.format(color=color))
        db_query['color'] = colors_with_hash

    if 'starRating' in query_args:
        db_query['starRating'] = {'$gt': query_args['starRating']}
    sort_param = 'createdAt'
    sort_direction = pymongo.DESCENDING
    if 'sort' in query_args:
        sort_direction = pymongo.ASCENDING if query_args['sort'] == 'asc' else pymongo.DESCENDING
        sort_param = 'price'
    return db_query, sort_param, sort_direction


def delete_all() -> Optional[Dict[str, str]]:
    try:
        result = dbconn.items_collection.delete_many({})
        return {'message': 'Deleted count: {count}'.format(count=result.deleted_count)}
    except Exception as e:
        return None
