import os
import asyncio
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.postgres import PostgresTools
from agno.tools.firecrawl import FirecrawlTools
from agno.memory import MemoryManager
from agno.knowledge.knowledge import Knowledge
from storage.ChromaStorage import ChromaStorage
from agno.vectordb.chroma import ChromaDb
from agno.knowledge.embedder.huggingface import HuggingfaceCustomEmbedder

class AiAgent:
	def __init__(self):

		self.embedder = HuggingfaceCustomEmbedder(id="all-MiniLM-L6-v2")

		self.llm = Gemini(
			id=os.getenv("MODEL_NAME")
		)


		self.knowledge = Knowledge(
			name="accounting_documents_kb",
			description="Contains the content of user-uploaded documents like invoices, receipts, and spreadsheets.",
			vector_db=ChromaDb(
				collection="accounting",
				path="/app/src/accounting_db",
				persistent_client=True,
				embedder=self.embedder
			)
		)

		self.tools = [
			FirecrawlTools(enable_scrape=True, enable_crawl=True),
			PostgresTools(
				host="postgres",
				port=5432,
				db_name="accounting_database",
				user="postgres",
				password="ggwhatthefuck123"
			)
		]

		self.memory_manager = MemoryManager()


		self.agent = Agent(
			model=self.llm,
			tools=self.tools,
			knowledge=self.knowledge, # <-- Pass the knowledge base here
			markdown=True,
			memory_manager=self.memory_manager,
			instructions="You are a helpful accounting assistant. First, check your knowledge base for information from user-uploaded files. If you can't find an answer there, you can use your other tools to query the database or browse the web."
		)

		print("AiAgent initialized with ChromaDB Knowledge Base.")

	async def run(self, query: str):
		return self.agent.run(query)