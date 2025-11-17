import os
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import (
	PyPDFLoader,
	Docx2txtLoader,
	TextLoader,
	CSVLoader,
	UnstructuredExcelLoader,
	UnstructuredImageLoader
)

class FileProcessor:
	def __init__(self):
		# Mapping file extensions to their LangChain loader class
		self.loaders = {
			".pdf": PyPDFLoader,
			".docx": Docx2txtLoader,
			".doc": Docx2txtLoader,
			".txt": TextLoader,
			".csv": CSVLoader,
			".xlsx": UnstructuredExcelLoader,
			".xls": UnstructuredExcelLoader,
			".png": UnstructuredImageLoader,
			".jpg": UnstructuredImageLoader 
		}

	def process_file(self, file_path: str) -> Document:

		if not os.path.exists(file_path):
			raise FileNotFoundError(f"File not found at path: {file_path}")

		_, file_extension = os.path.splitext(file_path)
		file_extension = file_extension.lower()

		loader_class = self.loaders.get(file_extension)

		if not loader_class:
			raise ValueError(f"Unsupported file type: '{file_extension}'")

		try:
			# All loaders have a simple .load() method
			loader = loader_class(file_path)
			docs = loader.load()

			if not docs:
				return Document(page_content="", metadata={"source": self.file_path})

			combined_content = "\n\n".join([doc.page_content for doc in docs])

			return Document(page_content=combined_content, metadata=docs[0].metadata)

		except Exception as e:
			raise RuntimeError(f"Failed to load file {file_path} with {loader_class.__name__}: {e}")