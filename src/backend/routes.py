from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from backend import controllers
from backend import models

router = APIRouter()

@router.post("/query")
async def run_query(query: models.Query):
	"""
	API Endpoint to run a query.
	It receives a request body matching the Query model.
	"""
	try:
		result = await controllers.process_query(query.query)
		return {"result": result.content}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload", response_model=models.UploadResponse)
async def upload_file(file: UploadFile = File(...)):
	"""
	API Endpoint to upload and process a file.
	"""
	try:
		result = controllers.process_and_store_file(file)
		return result

	except ValueError as e:
		raise HTTPException(status_code=400, detail=str(e))
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


@router.get("/get_all_docs")
async def get_all_documents_from_chroma():
	"""
	API Endpoint to get all documents from the ChromaDB collection.
	Useful for debugging and visualization.
	"""
	try:
		documents = controllers.get_all_chroma_documents()
		return documents
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@router.delete("/erase_all_docs")
async def erase_all_data_for_debugging():
	"""
	API Endpoint to erase all documents from MongoDB and ChromaDB.
	**USE WITH CAUTION: This is a destructive operation.**
	"""
	try:
		controllers.erase_all_documents()
		return "all documents erased successfully"
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"An unexpected error occurred during erasure: {str(e)}")