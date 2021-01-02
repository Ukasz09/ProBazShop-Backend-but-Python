item_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'description': {'type': 'string'},
        'imageURL': {'type': 'string'},
        'size': {'type': 'string'},
        'color': {'type': 'string'},
        'price': {'type': 'number'},
        'starRating': {'type': 'number'},
        'category': {'type': 'string'},
        'availableQty': {'type': 'integer'},
    },
    'required': [
        'name', 'description', 'imageURL', 'size', 'color', 'price', 'starRating', 'category',
        'availableQty'
    ]
}

user_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'surname': {'type': 'string'},
        'email': {'type': 'string'},
        'password': {'type': 'string'},
        'type': {'type': 'string'},
        'history': {
            "type": "array",
            "items": {'type': 'object',
                      'properties': {
                          'name': {'type': 'string'},
                          'description': {'type': 'string'},
                          'imageURL': {'type': 'string'},
                          'size': {'type': 'string'},
                          'color': {'type': 'string'},
                          'pricePerItem': {'type': 'number'},
                          'orderedQty': {'type': 'integer'},
                          'orderDate': {'type': 'string'},
                      },
                      'required': [
                          'name',
                          'description',
                          'imageURL',
                          'size',
                          'color',
                          'pricePerItem',
                          'orderedQty',
                          'orderDate',
                      ]}
        },
    },
    'required': ['name', 'surname', 'email', 'password', 'type', 'history']
}
