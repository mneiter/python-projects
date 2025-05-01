import logging
import time
from services.mongodb_service import MongoDBService
from pymongo.errors import ConnectionFailure, OperationFailure
from logger import get_logger

class MongoDBConsumerService:
    def __init__(self, logger=None):
        try:
            self.logger = logger or get_logger(self.__class__.__name__)
            self.mongo_service = MongoDBService()
        except Exception as e:
            logging.error(f"Failed to initialize MongoDBConsumerService: {e}")
            raise

    def consume_documents(self, stop_event):
        """Periodically fetch documents from MongoDB and print them."""
        try:
            while not stop_event.is_set():
                documents = self.mongo_service.db['kafka_messages'].find()
                
                self.logger.info("Fetched documents from MongoDB:")
                for doc in documents:
                    self.logger.info(doc)
                
                time.sleep(5)  # Sleep 5 seconds before next fetch
        except ConnectionFailure:
            self.logger.error("MongoDB connection failed")
        except OperationFailure as e:
            self.logger.error(f"MongoDB operation failed: {e}")
        except Exception as e:
            self.logger.error(f"Error consuming MongoDB documents: {e}")
        finally:
            self.mongo_service.client.close()
            self.logger.info("MongoDB Consumer stopped.")

    def consume_mongodb_examples(self):        
        self.mongodb_data()
        self.logger.info("MongoDB data inserted.")
        self.logger.info("Fetching documents from MongoDB...")
        
        self.get_mongodb_documents()

        self.aggregate_and_sort_message_counts()

        

    def aggregate_and_sort_message_counts(self):
        pipeline = [
            {"$group": {"_id": "$number", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        self.logger.info("Aggregating and sorting message counts...")
        self.logger.info(f"Pipeline: {pipeline}")
        
        aggregation_result = self.mongo_service.aggregate_documents('kafka_messages', pipeline)

        for doc in aggregation_result:
            self.logger.info(f"Aggregated document: {doc}")

    def get_mongodb_documents(self):
        docs = self.mongo_service.find_documents(
            collection_name='kafka_messages',
            filter_query={"number": {"$gt": 10}},
            limit=5,
            skip=0,
            sort_by="timestamp",
            descending=True
        )

        for doc in docs:
            self.logger.info(f"Document fetched: {doc}")

    def mongodb_data(self):
        self.mongo_service.insert_document('kafka_messages', {'number': 5, 'timestamp': '2025-04-23 18:00:00'})
        self.mongo_service.insert_document('kafka_messages', {'number': 10, 'timestamp': '2025-04-23 18:00:00'})
        self.mongo_service.insert_document('kafka_messages', {'number': 15, 'timestamp': '2025-04-23 18:00:00'})
        self.mongo_service.insert_document('kafka_messages', {'number': 20, 'timestamp': '2025-04-23 18:00:00'})
        self.mongo_service.insert_document('kafka_messages', {'number': 25, 'timestamp': '2025-04-23 18:00:00'})

