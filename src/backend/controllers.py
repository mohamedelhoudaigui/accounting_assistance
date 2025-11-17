import os
import shutil
from fastapi import UploadFile
from agent.agent_setup import AiAgent
from storage.FileProcessor import FileProcessor
from storage.ChromaStorage import ChromaStorage

from backend import models

agent = AiAgent()
file_processor = FileProcessor()
chroma_db = ChromaStorage()

# ------------- Agent intercation routes:

async def process_query(query: str) -> dict | list | str:
	"""
	Controller logic to run a query through the AI agent.
	"""
	result = await agent.run(query)
	return result


#----------data storage routes:

def process_and_store_file(file: UploadFile):
	"""
	Controller logic to save, process, and store a file.
	"""
	file_path = os.path.join("/tmp", file.filename)

	with open(file_path, "wb") as buffer:
		shutil.copyfileobj(file.file, buffer)

	try:
		processed_document = file_processor.process_file(file_path)
		chroma_db.add_document(processed_document)

		return {
			"filename": file.filename,
			"detail": "File processed and stored successfully."
		}

	finally:
		if os.path.exists(file_path):
			os.remove(file_path)


#--------------chroma db routes:

def get_all_chroma_documents():
	"""
	Controller logic to fetch all documents from the ChromaDB collection.
	"""
	documents = chroma_db.get_all_documents()
	return documents

def erase_all_documents():
	"""
	Controller logic to erase all documents from ChromaDB.
	"""
	deleted_chroma_count = chroma_db.delete_all_documents()

	return {
		"status": "success",
		"detail": "All collections have been cleared.",
		"deleted_from_chroma_chunks": deleted_chroma_count
	}