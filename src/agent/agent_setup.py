import os
import asyncio
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.postgres import PostgresTools
from agno.tools.firecrawl import FirecrawlTools
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb
from agno.knowledge.embedder.huggingface import HuggingfaceCustomEmbedder

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
			markdown=True,
			instructions=("You are an expert accounting assistant. Your primary goal is to provide accurate answers based on the user's data.\n"
						"1. **Always check the knowledge base first.** The knowledge base contains the content of the user's private, uploaded files. Use it to answer questions about specific invoices, expenses, or other document details.\n"
						"2. **If the knowledge base doesn't have the answer, query the PostgreSQL database.** The database contains structured data about invoices (`sage_invoices`, `invoice_lines`) and contacts (`contacts`). Use your SQL tools to query this data for totals, summaries, or specific records.\n"
						"3. **Only use the web browser if the question is general** and cannot be answered by the user's documents or the database (e.g., 'What are the current tax regulations in Morocco?').\n"
						"4. When presenting data, especially financial data, be precise and clear. If you are providing data from a document, mention the source.")
		)

		print("AiAgent initialized with ChromaDB Knowledge Base.")

	async def run(self, query: str):
		return self.agent.run(query)