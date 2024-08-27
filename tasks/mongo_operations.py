from .mongodb import MongoDBClient
from bson.objectid import ObjectId


def get_items(user_id=None, collection_name='tasks'):
    db = MongoDBClient.get_database()
    collection = db[collection_name]
    return collection.find({
        'user_id': user_id
    })


def find_one(user_id=None, id=None, collection_name='tasks'):
    db = MongoDBClient.get_database()
    collection = db[collection_name]
    return collection.find_one(
        {'_id': ObjectId(id), 'user_id': user_id}
    )


def insert_item(user_id=None, data=None, collection_name='tasks'):
    db = MongoDBClient.get_database()
    collection = db[collection_name]
    result = collection.insert_one({
            'title': data['title'],
            'description': data['description'],
            'creation_date': data['creation_date'],
            'due_date': data['due_date'],
            'status': data['status'],
            'user_id': user_id
        })
    return result


def update_item(user_id=None, id=None, item_data=None, collection_name='tasks'):
    db = MongoDBClient.get_database()
    collection = db[collection_name]
    result = collection.update_one(
        {'_id': ObjectId(id), 'user_id': user_id},
        {
            '$set': {
                'title': item_data['title'],
                'description': item_data['description'],
                'due_date': item_data['due_date'],
                'status': item_data['status'],
                'user_id': user_id
            }
        }
    )
    return result


def delete_one(user_id=None, id=None, collection_name='tasks'):
    db = MongoDBClient.get_database()
    collection = db[collection_name]
    result = collection.delete_one(
        {'_id': ObjectId(id), 'user_id': user_id}
    )
    return result
