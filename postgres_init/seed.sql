-- seed_data.sql
-- Insert mock data into the Sage Invoice System

-- First, insert contacts
INSERT INTO contacts (name, address_line_1, address_line_2, city, postal_code, country) VALUES
('Mohamed Alami', '123 Avenue Hassan II', 'Appt 4B', 'Casablanca', '20000', 'Morocco'),
('Fatima Zahra', '45 Rue Mohammed V', NULL, 'Rabat', '10000', 'Morocco'),
('Karim Benjelloun', '78 Boulevard Mohamed VI', 'Floor 3', 'Marrakech', '40000', 'Morocco'),
('Amina Toumi', '22 Rue des Orangers', NULL, 'Tangier', '90000', 'Morocco'),
('Youssef El Fassi', '56 Avenue des FAR', 'Building C', 'Fes', '30000', 'Morocco'),
('Sophie Martin', '89 Rue de Paris', NULL, 'Paris', '75001', 'France'),
('John Smith', '123 Main Street', 'Suite 500', 'New York', '10001', 'USA'),
('Maria Garcia', 'Avenida de la Luz 45', 'Piso 2', 'Madrid', '28001', 'Spain');

-- Insert main invoices
INSERT INTO sage_invoices (invoice_number, contact_id, date, due_date, reference, notes, subtotal, total_tax_amount, total_amount, currency) VALUES
('INV-2024-001', 1, '2024-01-15', '2024-02-15', 'PO-12345', 'Monthly consulting services', 5000.00, 1000.00, 6000.00, 'MAD'),
('INV-2024-002', 2, '2024-01-20', '2024-02-20', 'PO-12346', 'Web development project', 8000.00, 1600.00, 9600.00, 'MAD'),
('INV-2024-003', 3, '2024-02-01', '2024-03-01', 'PO-12347', 'Marketing campaign Q1', 12000.00, 2400.00, 14400.00, 'MAD'),
('INV-2024-004', 4, '2024-02-10', '2024-03-10', NULL, 'Regular maintenance', 3000.00, 600.00, 3600.00, 'MAD'),
('INV-2024-005', 5, '2024-02-15', '2024-03-15', 'PO-12348', 'Software license renewal', 7500.00, 1500.00, 9000.00, 'MAD'),
('INV-2024-006', 6, '2024-02-20', '2024-03-20', 'PO-12349', 'International project', 20000.00, 4000.00, 24000.00, 'EUR'),
('INV-2024-007', 7, '2024-03-01', '2024-04-01', 'PO-12350', 'US market expansion', 15000.00, 3000.00, 18000.00, 'USD'),
('INV-2024-008', 8, '2024-03-05', '2024-04-05', 'PO-12351', 'Spanish localization', 9000.00, 1800.00, 10800.00, 'EUR');

-- Insert invoice lines for INV-2024-001
INSERT INTO invoice_lines (invoice_id, description, quantity, unit_price, discount_amount, tax_amount, total_amount) VALUES
(1, 'Consulting hours - Strategy', 20, 200.00, 0.00, 400.00, 4000.00),
(1, 'Consulting hours - Implementation', 10, 100.00, 0.00, 100.00, 1000.00);

-- Insert invoice lines for INV-2024-002
INSERT INTO invoice_lines (invoice_id, description, quantity, unit_price, discount_amount, tax_amount, total_amount) VALUES
(2, 'Frontend development', 50, 120.00, 0.00, 1200.00, 6000.00),
(2, 'Backend development', 20, 100.00, 0.00, 400.00, 2000.00),
(2, 'Project management', 10, 60.00, 0.00, 120.00, 600.00);

-- Insert invoice lines for INV-2024-003
INSERT INTO invoice_lines (invoice_id, description, quantity, unit_price, discount_amount, tax_amount, total_amount) VALUES
(3, 'Social media campaign', 1, 8000.00, 500.00, 1500.00, 7500.00),
(3, 'Google Ads management', 1, 3000.00, 0.00, 600.00, 3000.00),
(3, 'Content creation', 10, 150.00, 0.00, 300.00, 1500.00);

-- Insert invoice lines for INV-2024-004
INSERT INTO invoice_lines (invoice_id, description, quantity, unit_price, discount_amount, tax_amount, total_amount) VALUES
(4, 'Monthly maintenance - Basic', 1, 2000.00, 0.00, 400.00, 2000.00),
(4, 'Emergency support', 2, 500.00, 0.00, 200.00, 1000.00);

-- Insert invoice lines for INV-2024-005
INSERT INTO invoice_lines (invoice_id, description, quantity, unit_price, discount_amount, tax_amount, total_amount) VALUES
(5, 'Enterprise license', 5, 1200.00, 300.00, 1050.00, 5250.00),
(5, 'Support package', 1, 1500.00, 0.00, 300.00, 1500.00),
(5, 'Training sessions', 3, 250.00, 0.00, 150.00, 750.00);

-- Insert invoice lines for INV-2024-006
INSERT INTO invoice_lines (invoice_id, description, quantity, unit_price, discount_amount, tax_amount, total_amount) VALUES
(6, 'International consulting', 100, 150.00, 0.00, 3000.00, 15000.00),
(6, 'Market research', 1, 3000.00, 0.00, 600.00, 3000.00),
(6, 'Translation services', 20, 100.00, 0.00, 400.00, 2000.00);

-- Insert invoice lines for INV-2024-007
INSERT INTO invoice_lines (invoice_id, description, quantity, unit_price, discount_amount, tax_amount, total_amount) VALUES
(7, 'US market analysis', 1, 8000.00, 0.00, 1600.00, 8000.00),
(7, 'Legal consultation', 10, 500.00, 0.00, 1000.00, 5000.00),
(7, 'Business development', 20, 100.00, 0.00, 400.00, 2000.00);

-- Insert invoice lines for INV-2024-008
INSERT INTO invoice_lines (invoice_id, description, quantity, unit_price, discount_amount, tax_amount, total_amount) VALUES
(8, 'Spanish translation', 500, 15.00, 0.00, 1500.00, 7500.00),
(8, 'Cultural adaptation', 10, 100.00, 0.00, 200.00, 1000.00),
(8, 'Quality assurance', 5, 60.00, 0.00, 60.00, 300.00);

-- Insert some additional invoices for variety
INSERT INTO sage_invoices (invoice_number, contact_id, date, due_date, reference, notes, subtotal, total_tax_amount, total_amount, currency) VALUES
('INV-2024-009', 1, '2024-03-10', '2024-04-10', 'PO-12352', 'Additional consulting', 2500.00, 500.00, 3000.00, 'MAD'),
('INV-2024-010', 3, '2024-03-15', '2024-04-15', 'PO-12353', 'Q2 marketing prep', 6000.00, 1200.00, 7200.00, 'MAD');

INSERT INTO invoice_lines (invoice_id, description, quantity, unit_price, discount_amount, tax_amount, total_amount) VALUES
(9, 'Strategic planning session', 5, 400.00, 0.00, 400.00, 2000.00),
(9, 'Follow-up consultation', 2, 250.00, 0.00, 100.00, 500.00),
(10, 'Market analysis Q2', 1, 4000.00, 0.00, 800.00, 4000.00),
(10, 'Creative development', 10, 200.00, 0.00, 400.00, 2000.00);

-- Display summary of inserted data
SELECT 
    (SELECT COUNT(*) FROM contacts) as total_contacts,
    (SELECT COUNT(*) FROM sage_invoices) as total_invoices,
    (SELECT COUNT(*) FROM invoice_lines) as total_invoice_lines;