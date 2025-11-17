from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class Query(BaseModel):
    query: str

class UploadResponse(BaseModel):
    filename: str
    detail: str
