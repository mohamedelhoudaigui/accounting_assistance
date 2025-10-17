import chromadb
import os


class ChromaStorage:

	def __init__(self):
		self.chroma_client = chromadb.PersistentClient(path=os.getenv('db_path'))
		self.collection = self.chroma_client.get_or_create_collection(name=os.getenv('collection_name'))

	def add_to_collection(document_object):
		self.collection.add(document_object)
