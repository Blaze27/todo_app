from pymongo import MongoClient
from django.conf import settings
import os


class MongoDBClient:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            cls._client = MongoClient(
                host=os.getenv('MONGO_HOST', settings.MONGO_DB_HOST),
                port=int(os.getenv('MONGO_PORT', settings.MONGO_DB_PORT)),
                username=os.getenv('MONGO_USER', 'root'),
                password=os.getenv('MONGO_PASSWORD', 'example')
            )
        return cls._client

    @classmethod
    def get_database(cls):
        client = cls.get_client()
        return client[settings.MONGO_DB_NAME]
