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

# Mount the static files directory
# This will serve files from 'src/frontend' under the '/static' path
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """
    Serve the main HTML file for the chat interface.
    """
    with open("frontend/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)