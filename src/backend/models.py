from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class Query(BaseModel):
    query: str


class UploadResponse(BaseModel):
    filename: str
    detail: str


class InvoiceLine(BaseModel):
    """
    Represents a single line item on a Sage invoice.
    """
    description: str
    quantity: float
    unit_price: float
    discount_amount: Optional[float] = None
    tax_amount: float
    total_amount: float

class Contact(BaseModel):
    """
    Represents the contact details for the customer.
    """
    name: str
    address_line_1: str
    address_line_2: Optional[str] = None
    city: str
    postal_code: str
    country: str

class SageInvoice(BaseModel):
    """
    A Pydantic model representing a customer invoice in Sage Accounting.
    """
    invoice_number: str
    contact: Contact
    date: date
    due_date: date
    reference: Optional[str] = None
    notes: Optional[str] = None
    invoice_lines: List[InvoiceLine]
    subtotal: float
    total_tax_amount: float
    total_amount: float
    currency: str = "MAD"