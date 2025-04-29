import logging
import time
from mongodb_service import MongoDBService
from pymongo.errors import ConnectionFailure, OperationFailure

class MongoDBConsumerService:
    def __init__(self):
        self.mongo_service = MongoDBService()
        self.logger = logging.getLogger(self.__class__.__name__)

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