from pymongo import MongoClient
import logging

class MongoDBService:
    def __init__(self, host='localhost', port=27017, db_name='testdb'):
        try:
            self.client = MongoClient(host, port)
            self.db = self.client[db_name]
            self.logger = logging.getLogger(self.__class__.__name__)
            self.logger.info(f"Connected to MongoDB at {host}:{port}, DB: {db_name}")
        except Exception as e:
            self.logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    def insert_document(self, collection_name, document):
        try:
            collection = self.db[collection_name]
            result = collection.insert_one(document)
            self.logger.info(f"Inserted document with ID: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            self.logger.error(f"Failed to insert document: {e}")
            raise
