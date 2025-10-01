-- init.sql
-- Create tables for Sage Invoice System

CREATE TABLE contacts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address_line_1 VARCHAR(255) NOT NULL,
    address_line_2 VARCHAR(255),
    city VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    country VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sage_invoices (
    id SERIAL PRIMARY KEY,
    invoice_number VARCHAR(100) UNIQUE NOT NULL,
    contact_id INTEGER NOT NULL,
    date DATE NOT NULL,
    due_date DATE NOT NULL,
    reference VARCHAR(255),
    notes TEXT,
    subtotal DECIMAL(15, 2) NOT NULL,
    total_tax_amount DECIMAL(15, 2) NOT NULL,
    total_amount DECIMAL(15, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'MAD',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_contact
        FOREIGN KEY (contact_id)
        REFERENCES contacts(id)
        ON DELETE CASCADE
);

CREATE TABLE invoice_lines (
    id SERIAL PRIMARY KEY,
    invoice_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    quantity DECIMAL(10, 2) NOT NULL,
    unit_price DECIMAL(15, 2) NOT NULL,
    discount_amount DECIMAL(15, 2),
    tax_amount DECIMAL(15, 2) NOT NULL,
    total_amount DECIMAL(15, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_invoice
        FOREIGN KEY (invoice_id)
        REFERENCES sage_invoices(id)
        ON DELETE CASCADE
);

-- Create indexes for better performance
CREATE INDEX idx_invoice_lines_invoice_id ON invoice_lines(invoice_id);
CREATE INDEX idx_sage_invoices_contact_id ON sage_invoices(contact_id);
CREATE INDEX idx_sage_invoices_invoice_number ON sage_invoices(invoice_number);
CREATE INDEX idx_sage_invoices_date ON sage_invoices(date);

-- Create a function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers to automatically update updated_at
CREATE TRIGGER update_contacts_updated_at
    BEFORE UPDATE ON contacts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_sage_invoices_updated_at
    BEFORE UPDATE ON sage_invoices
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();