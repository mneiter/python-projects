from config import MONGODB_URI, LOG_DIR, LOG_FILE
from pymongo import MongoClient, ASCENDING, DESCENDING
import logging
from pymongo.errors import ConnectionFailure, OperationFailure

class MongoDBService:
    def __init__(self, host=MONGODB_URI, port=27017, db_name='testdb'):
        try:
            self.client = MongoClient(host, port)

            self.client = MongoClient(
                host=host,
                port=port,
                serverSelectionTimeoutMS=5000,  # Timeout for initial connection
                socketTimeoutMS=5000,            # Timeout for operations
                connectTimeoutMS=5000,            # Timeout for connecting
                retryWrites=True
            )

            self.client.admin.command('ping') # Test the connection
            self.db = self.client[db_name]
            self.logger = logging.getLogger(self.__class__.__name__)
            self.logger.info(f"Connected to MongoDB at {host}:{port}, DB: {db_name}")

            self.create_indexes() # Create indexes if needed
        except ConnectionFailure:
            self.logger.error("Failed to connect to MongoDB server.")
            raise
        except OperationFailure as e:
            self.logger.error(f"MongoDB operation error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    def create_indexes(self):
        """Create indexes for commonly queried fields."""
        try:
            self.db['kafka_messages'].create_index([("timestamp", DESCENDING)])
            self.db['kafka_messages'].create_index([("number", ASCENDING)])
            self.logger.info("Indexes created on 'timestamp' and 'number'.")
        except Exception as e:
            self.logger.error(f"Failed to create indexes: {e}")

    def insert_document(self, collection_name, document):
        """Insert a single document into the collection."""
        try:
            collection = self.db[collection_name]
            result = collection.insert_one(document)
            self.logger.info(f"Inserted document ID: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            self.logger.error(f"Failed to insert document: {e}")
            raise

    def find_documents(self, collection_name, filter_query=None, limit=10, skip=0, sort_by="timestamp", descending=True):
        """Find documents with optional filter, pagination, and sorting."""
        try:
            collection = self.db[collection_name]
            sort_order = DESCENDING if descending else ASCENDING
            cursor = collection.find(filter_query or {}).sort(sort_by, sort_order).skip(skip).limit(limit)
            documents = list(cursor)
            self.logger.info(f"Fetched {len(documents)} documents from '{collection_name}'.")
            return documents
        except Exception as e:
            self.logger.error(f"Failed to fetch documents: {e}")
            raise

    def aggregate_documents(self, collection_name, pipeline):
        """Run an aggregation pipeline."""
        try:
            collection = self.db[collection_name]
            results = list(collection.aggregate(pipeline))
            self.logger.info(f"Aggregated {len(results)} documents from '{collection_name}'.")
            return results
        except Exception as e:
            self.logger.error(f"Failed to aggregate documents: {e}")
            raise

    def close(self):
        """Close the MongoDB client connection."""
        if self.client:
            self.client.close()
            self.logger.info("MongoDB connection closed.")