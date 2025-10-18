import chromadb
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChromaStorage:
	def __init__(self):

		self.dir = os.getenv('DB_PATH')
		self.collection_name = os.getenv('COLLECTION_NAME')

		if not self.dir or not self.collection_name:
			raise ValueError("DB_PATH and COLLECTION_NAME environment variables must be set")

		self.chroma_client = chromadb.PersistentClient(path=self.dir)
		self.collection = self.chroma_client.get_or_create_collection(name=self.collection_name)
		logger.info("ChromaDB connection successful.")


	def add_to_collection(self, document_object: dict, mongo_id: str):

		ids = []
		documents = []

		ids.append(document_object.get("metadata"))
		documents.append(document_object.get("content"))

		self.collection.add(
			ids=ids,
			documents=documents
		)

		logger.info("added document to chroma dn successfully")



	def get_all_documents(self):
		"""
		Retrieves all documents and their metadata from the ChromaDB collection.
		
		Returns:
			A dictionary containing all data from the collection.
		"""
		return self.collection.get()