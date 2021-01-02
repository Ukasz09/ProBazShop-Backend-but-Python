import dbconn
from typing import Dict, Any


def create(request: Dict[str, Any]) -> Dict[str, str]:
    result = dbconn.items_collection.insert_one(request)
    inserted_item = dbconn.items_collection.find({'_id': result.inserted_id}, {'_id': False})[0]
    inserted_item['id'] = str(result.inserted_id)
    return inserted_item
