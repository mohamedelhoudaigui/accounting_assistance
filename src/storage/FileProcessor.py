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

    def process_file(self, file_path: str) -> List[Document]:
        """
        Processes a file using the appropriate LangChain document loader.

        Args:
            file_path (str): The path to the file.

        Returns:
            A list of LangChain Document objects, each representing the file's content.
        """

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
            documents = loader.load()
            return documents
        except Exception as e:
            # This provides better error feedback
            raise RuntimeError(f"Failed to load file {file_path} with {loader_class.__name__}: {e}")