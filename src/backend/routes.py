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


@router.get("/invoices")
async def get_invoices():
	"""
	API Endpoint to get all invoices.
	"""
	try:
		documents = await controllers.get_all_invoices()
		return documents
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@router.get("/contacts")
async def get_contacts():
	"""
	API Endpoint to get all contacts.
	"""
	try:
		contacts = await controllers.get_all_contacts()
		return contacts
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@router.get("/invoice_lines")
async def get_invoice_lines():
	"""
	API Endpoint to get all invoice_lines.
	"""
	try:
		invoice_lines = await controllers.get_all_invoice_lines()
		return invoice_lines
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@router.post("/create_invoice")
async def create_invoice(invoice: models.SageInvoice):
	"""
	API Endpoint to create a new invoice in the database.
	"""
	try:
		result = await controllers.create_new_invoice(invoice)
		return result
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


@router.get("/chroma/all")
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


@router.get("/mongo/all")
async def get_all_documents_from_mongo():
	"""
	API endpoint to get all documents from mongo db.
	"""
	try:
		documents = controllers.get_all_mongo_documents()
		return documents

	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@router.delete("/debug/erase-all", status_code=200)
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