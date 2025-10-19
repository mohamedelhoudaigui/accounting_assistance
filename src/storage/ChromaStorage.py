import os
import logging
from typing import List
from langchain_core.documents import Document

# High-level LangChain components for vector store management
from langchain_chroma import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChromaStorage:
    def __init__(self):
        """
        Initializes the ChromaStorage service, setting up the embedding model,
        text splitter, and the Chroma vector store itself.
        """
        self.db_path = os.getenv('DB_PATH')
        self.collection_name = os.getenv('COLLECTION_NAME')
        os.makedirs(self.db_path, exist_ok=True)

        self.embedding_function = SentenceTransformerEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        self.vector_store = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embedding_function,
            persist_directory=self.db_path,
        )

        logger.info(f"ChromaDB vector store initialized for collection '{self.collection_name}'.")

    def add_documents(self, documents: List[Document]):
        """
        Splits, embeds, and stores a list of LangChain Documents in ChromaDB.
        This is the primary method for adding new file content to the RAG system.
        """
        if not documents:
            logger.warning("No documents provided to add to the collection.")
            return

        split_docs = self.text_splitter.split_documents(documents)

        self.vector_store.add_documents(split_docs)
        logger.info(f"Successfully processed and added {len(split_docs)} document chunks to ChromaDB.")

    def get_all_documents(self):
        """
        Retrieves all document chunks from the ChromaDB collection.
        Useful for debugging.
        """

        return self.vector_store.get(include=["metadatas", "documents"])

    def delete_all_documents(self):
        """
        Deletes and re-creates the entire ChromaDB collection to erase all documents.
        """
        try:
            count = self.vector_store._collection.count()
            self.vector_store.delete_collection()
            logger.info(f"Deleted ChromaDB collection '{self.collection_name}' with {count} documents.")

            self.vector_store = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embedding_function,
                persist_directory=self.db_path,
            )
            logger.info(f"Re-created empty ChromaDB collection '{self.collection_name}'.")
            return count
        except Exception as e:
            logger.error(f"Failed to delete and re-create ChromaDB collection: {e}")
            return 0