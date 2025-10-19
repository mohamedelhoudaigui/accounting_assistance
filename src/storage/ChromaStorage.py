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
        self.db_path = os.getenv('DB_PATH', 'lancedb')
        self.collection_name = os.getenv('COLLECTION_NAME', 'accounting_docs')
        os.makedirs(self.db_path, exist_ok=True)

        # 1. Initialize the embedding model. This will be used to convert text to vectors.
        #    'all-MiniLM-L6-v2' is a fantastic, lightweight default model that runs locally.
        self.embedding_function = SentenceTransformerEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )

        # 2. Initialize a text splitter. This will break large documents from the loaders
        #    into smaller, more effective chunks for semantic search.
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,  # The size of each chunk in characters
            chunk_overlap=200   # The number of characters to overlap between chunks
        )

        # 3. Initialize the Chroma vector store. This object is our main interface to ChromaDB.
        #    It uses the embedding function and will persist data to the specified directory.
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

        # First, split the loaded documents into smaller, manageable chunks.
        split_docs = self.text_splitter.split_documents(documents)

        # Now, add the split documents to the vector store.
        # LangChain handles the embedding process automatically using the function we provided.
        self.vector_store.add_documents(split_docs)
        logger.info(f"Successfully processed and added {len(split_docs)} document chunks to ChromaDB.")

    def get_all_documents(self):
        """
        Retrieves all document chunks from the ChromaDB collection.
        Useful for debugging.
        """
        # The .get() method on the vector store object retrieves data.
        # We include metadatas and documents for a complete, human-readable view.
        return self.vector_store.get(include=["metadatas", "documents"])

    def delete_all_documents(self):
        """
        Deletes and re-creates the entire ChromaDB collection to erase all documents.
        """
        try:
            count = self.vector_store._collection.count()
            self.vector_store.delete_collection()
            logger.info(f"Deleted ChromaDB collection '{self.collection_name}' with {count} documents.")

            # Re-initialize the vector store to create a new, empty collection
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