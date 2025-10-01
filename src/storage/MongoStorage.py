import os
from pymongo import MongoClient
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoStorage:
    def __init__(self):
        # Construct the connection string from environment variables
        self.client = MongoClient(
            host=os.getenv("MONGO_HOST"),
            port=int(os.getenv("MONGO_PORT")),
            username=os.getenv("MONGO_USER"),
            password=os.getenv("MONGO_PASSWORD"),
        )
        self.db = self.client[os.getenv("MONGO_DB")]
        logger.info("MongoDB connection established.")

    def close(self):
        """Closes the connection to the database."""
        self.client.close()
        logger.info("MongoDB connection closed.")

    def insert_doc(self, data: dict, collection_name: str):
        """
        Inserts a document into the specified collection.

        Args:
            data (dict): The document to insert.
            collection_name (str): The name of the collection.

        Returns:
            The ID of the inserted document.
        """
        collection = self.db[collection_name]
        result = collection.insert_one(data)
        return result.inserted_id