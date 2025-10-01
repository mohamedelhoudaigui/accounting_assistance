import os
from psycopg_pool import AsyncConnectionPool
from psycopg.rows import dict_row
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PostgresDataStorage:
    def __init__(self):
        conninfo = (
            f"host={os.getenv('POSTGRES_HOST')} "
            f"dbname={os.getenv('POSTGRES_DB')} "
            f"user={os.getenv('POSTGRES_USER')} "
            f"password={os.getenv('POSTGRES_PASSWORD')}"
        )
        # We use an AsyncConnectionPool for compatibility with FastAPI
        self.pool = AsyncConnectionPool(conninfo=conninfo, min_size=1, max_size=10)
        logger.info("PostgreSQL connection pool created.")

    async def close(self):
        await self.pool.close()
        logger.info("PostgreSQL connection pool closed.")


    async def fetch_all(self, query: str, params: tuple = None) -> list[dict]:
        """
        Executes a query and returns all results as a list of dictionaries.
        """
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute(query, params)
                result = await cur.fetchall()
                return result

    async def fetch_one(self, query: str, params: tuple = None) -> dict | None:
        """
        Executes a query and returns a single result as a dictionary.
        """
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute(query, params)
                result = await cur.fetchone()
                return result

    async def execute(self, query: str, params: tuple = None) -> int:
        """
        Executes a query (e.g., INSERT, UPDATE, DELETE) and returns the
        number of affected rows. The transaction is committed automatically.
        """
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, params)
                return cur.rowcount