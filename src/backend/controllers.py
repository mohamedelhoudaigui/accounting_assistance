import os
import shutil
from fastapi import UploadFile
from agent.agent_setup import AiAgent
from storage.FileProcessor import FileProcessor
from storage.PostgresStorage import PostgresDataStorage
from storage.MongoStorage import MongoStorage
from storage.ChromaStorage import ChromaStorage

from backend import models

agent = AiAgent()
file_processor = FileProcessor()
db = PostgresDataStorage()
mongo_db = MongoStorage()
chroma_db = ChromaStorage()

UPLOAD_DIR = "upload"


async def process_query(query: str) -> dict | list | str:
    """
    Controller logic to run a query through the AI agent.
    """
    result = await agent.run(query)
    return result


async def get_all_invoices():
    """
    Controller logic to fetch all invoices from the database.
    """
    query = "SELECT * FROM sage_invoices ORDER BY date DESC;"
    invoices = await db.fetch_all(query)
    return invoices


async def get_all_contacts():
    """
    Controller logic to fetch all invoices from the database.
    """
    query = "SELECT * FROM contacts ORDER BY created_at DESC;"
    contacts = await db.fetch_all(query)
    return contacts


async def get_all_invoice_lines():
    """
    Controller logic to fetch all invoices from the database.
    """
    query = "SELECT * FROM invoice_lines ORDER BY created_at DESC;"
    invoice_lines = await db.fetch_all(query)
    return invoice_lines


def process_and_store_file(file: UploadFile):
    """
    Controller logic to save, process, and store a file.
    """
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        processed_data = file_processor.process_file(file_path, mongo_db)
        if processed_data.get("error"):
            raise ValueError(processed_data.get("error"))

        mongo_db.insert_doc(processed_data)
        chroma_db.add_to_collection(processed_data)

        return {
            "filename": file.filename,
            "detail": "File processed and stored successfully."
        }

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


async def create_new_invoice(invoice: models.SageInvoice) -> dict:

    contact_query = """
        INSERT INTO contacts (name, address_line_1, address_line_2, city, postal_code, country)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id;
    """
    contact_params = (
        invoice.contact.name, invoice.contact.address_line_1, invoice.contact.address_line_2,
        invoice.contact.city, invoice.contact.postal_code, invoice.contact.country
    )

    contact_result = await db.fetch_one(contact_query, contact_params)
    contact_id = contact_result['id']
    invoice_query = """
        INSERT INTO sage_invoices (invoice_number, contact_id, date, due_date, reference, notes, subtotal, total_tax_amount, total_amount, currency)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
    """

    invoice_params = (
        invoice.invoice_number, contact_id, invoice.date, invoice.due_date, invoice.reference,
        invoice.notes, invoice.subtotal, invoice.total_tax_amount, invoice.total_amount, invoice.currency
    )
    invoice_result = await db.fetch_one(invoice_query, invoice_params)
    invoice_id = invoice_result['id']


    line_query = """
        INSERT INTO invoice_lines (invoice_id, description, quantity, unit_price, discount_amount, tax_amount, total_amount)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    for line in invoice.invoice_lines:
        line_params = (
            invoice_id, line.description, line.quantity, line.unit_price,
            line.discount_amount, line.tax_amount, line.total_amount
        )
        await db.execute(line_query, line_params)

    return {"status": "success", "invoice_id": invoice_id, "contact_id": contact_id}