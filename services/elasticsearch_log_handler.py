import logging
import json
import socket
from datetime import datetime
from elasticsearch import Elasticsearch
from config import IS_DOCKER, ENVIRONMENT

class ElasticsearchLogHandler(logging.Handler):
    def __init__(self, base_index="logs", host=None, port=9200, scheme="http", service="python-app"):
        super().__init__()
        self.base_index = base_index
        self.service = service
        self.environment = ENVIRONMENT
        self.hostname = socket.gethostname()
        self.es = Elasticsearch(f"{scheme}://{host or ('elasticsearch' if IS_DOCKER else 'localhost')}:{port}")

    def emit(self, record):
        try:
            # Format log record as JSON
            log_entry = {
                "@timestamp": datetime.utcnow().isoformat(),
                "level": record.levelname,
                "logger": record.name,
                "thread": record.threadName,
                "message": record.getMessage(),
                "module": record.module,
                "file": record.filename,
                "line": record.lineno,
                "function": record.funcName,
                "environment": self.environment,
                "service": self.service,
                "host": self.hostname
            }

            # Create date-based index
            index_name = f"{self.base_index}-{datetime.utcnow().strftime('%Y-%m-%d')}"
            self.es.index(index=index_name, document=log_entry)

        except Exception as e:
            # Fallback to stderr if Elasticsearch fails
            print(f"[ElasticsearchLogHandler] Failed to send log to ES: {e}", flush=True)
