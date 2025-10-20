import os
import asyncio
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.postgres import PostgresTools
from agno.tools.firecrawl import FirecrawlTools
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb
from agno.knowledge.embedder.huggingface import HuggingfaceCustomEmbedder
from agno.memory import MemoryManager

class AiAgent:
	def __init__(self):

		self.embedder = HuggingfaceCustomEmbedder(id="sentence-transformers/all-MiniLM-L6-v2")

		self.llm = Gemini(
			id=os.getenv("MODEL_NAME")
		)

		self.knowledge = Knowledge(
			name="accounting_documents_kb",
			description="Contains the content of user-uploaded documents like invoices, receipts, and spreadsheets.",
			vector_db=ChromaDb(
				collection=os.getenv('COLLECTION_NAME'),
				path=os.getenv('DB_PATH'),
				persistent_client=True,
				embedder=self.embedder
			)
		)

		self.memory_manager = MemoryManager()


		self.tools = [
			FirecrawlTools(enable_scrape=True, enable_crawl=True),
			PostgresTools(
				host=os.getenv("POSTGRES_HOST"),
				port=int(os.getenv("POSTGRES_PORT")),
				db_name=os.getenv("POSTGRES_DB"),
				user=os.getenv("POSTGRES_USER"),
				password=os.getenv("POSTGRES_PASSWORD")
			)
		]


		self.agent = Agent(
			add_knowledge_to_context=True,
			model=self.llm,
			tools=self.tools,
			knowledge=self.knowledge,
			memory_manager=self.memory_manager,
			markdown=True,
		)

		print("AiAgent initialized with ChromaDB Knowledge Base.")

	async def run(self, query: str):
		return self.agent.run(query)