import os
from pymongo import MongoClient
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoStorage:
    def __init__(self):
        mongo_uri = os.getenv("MONGO_URI")
        db_name = os.getenv("MONGO_DB")

        if not mongo_uri or not db_name:
            raise ValueError("MONGO_URI and MONGO_DB environment variables must be set")

        # Connect using the full URI
        self.client = MongoClient(mongo_uri)
        
        # Select the database
        self.db = self.client[db_name]
        
        # Optional: Verify connection by sending a ping
        try:
            self.client.admin.command('ping')
            logger.info("MongoDB connection successful.")
        except Exception as e:
            logger.error(f"MongoDB connection failed: {e}")
            raise

    def close(self):
        """Closes the connection to the database."""
        self.client.close()
        logger.info("MongoDB connection closed.")

    def insert_doc(self, data: dict):
        """
        Inserts a document into the specified collection.

        Args:
            data (dict): The document to insert.
            collection_name (str): The name of the collection.

        Returns:
            The ID of the inserted document.
        """
        collection = self.db["documents"]
        result = collection.insert_one(data)
        return result.inserted_id