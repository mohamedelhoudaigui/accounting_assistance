import asyncio
from dotenv import load_dotenv
import os
import logging
import sys

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from backend.routes import router as api_router

# Load environment variables at the start
load_dotenv()

app = FastAPI()

# Mount the API router
app.include_router(api_router)


@app.get("/")
async def read_root():
     return "server is launched !"