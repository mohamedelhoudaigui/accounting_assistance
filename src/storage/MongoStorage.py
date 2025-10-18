import os
from pymongo import MongoClient
import logging
from typing import List
from langchain_core.documents import Document

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


    def insert_langchain_documents(self, documents: List[Document], source_file: str):
        """
        Converts a list of LangChain documents into a single record and inserts it into MongoDB.

        Args:
            documents (List[Document]): The list of documents loaded by LangChain.
            source_file (str): The original filename.

        Returns:
            The ID of the inserted MongoDB record.
        """
        if not documents:
            return None

        # Create a single record that represents the entire file
        # The first document's metadata is often representative of the whole file
        record = {
            "source": source_file,
            "metadata": documents[0].metadata,
            "content": [
                {
                    "page_content": doc.page_content,
                    "metadata": doc.metadata
                }
                for doc in documents
            ]
        }

        collection = self.db["documents"]
        result = collection.insert_one(record)
        return result.inserted_id


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

    def get_all_docs(self):
        """
        Get all mongo db collection items from self.collection.
        """

        return self.db["documents"].find()