import os
import asyncio
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.postgres import PostgresTools
from agno.tools.firecrawl import FirecrawlTools
from agno.memory import MemoryManager

class AiAgent:
	def __init__(self):

		self.llm = Gemini(
			id=os.getenv("MODEL_NAME")
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
			model = self.llm,
			tools=self.tools,
			markdown=True,
			memory_manager=self.memory_manager
		)

	async def run(self, query: str):
		return self.agent.run(query)