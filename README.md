# Accounting Assistance AI

Hello there! Welcome to the Accounting Assistance AI project. This isn't your average, boring accounting software. Think of it as a smart helper that can chat with you about your financial documents, invoices, and even browse the web for information.

The goal is to make accounting tasks less of a chore and more of a conversation. You can upload your documents, ask questions in plain English, and get the information you need without digging through endless spreadsheets.

## About The Project

This project combines the power of Large Language Models (LLMs) with your own financial data. Here's a breakdown of what's going on under the hood:

*   **Conversational AI:** At its heart, there's a smart agent (powered by Google's Gemini) that you can talk to.
*   **Document Understanding:** You can upload various types of documents (PDFs, DOCX, XLSX, etc.). The system reads them, understands their content, and stores the information in a way the AI can access.
*   **Database Integration:** It connects to a PostgreSQL database that's set up to mirror a Sage accounting system. This means the AI can query your structured data, like invoices and customer contacts.
*   **Web Search:** If the answer isn't in your documents or the database, the AI can use Firecrawl to search the web.
*   **Solid Foundation:** The whole thing is neatly packaged with Docker, so you can get it up and running with just a couple of simple commands.

## Getting Started

Ready to give it a try? Here’s how to get everything set up.

### Prerequisites

You'll need to have Docker and Docker Compose installed on your machine. That's pretty much it!

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/mohamedelhoudaigui/accounting_assistance.git
    cd accounting_assistance
    ```

2.  **Set up your environment variables:**
    There's a file called `env_example`. Make a copy of it and name it `.env`.
    ```sh
    cp env_example .env
    ```
    Now, open that new `.env` file with a text editor. You'll need to **add your API keys** for the AI to function correctly.

    *   `GOOGLE_API_KEY`: Your API key for Google's Generative AI services (Gemini). You can get this from [Google AI Studio](https://aistudio.google.com/app/apikey).
    *   `FIRECRAWL_API_KEY`: (Optional) If you want the agent to be able to browse the web, you'll need a key from [Firecrawl](https://www.firecrawl.dev/).
    *   `HUGGING_FACE_HUB_TOKEN`: (Optional, but recommended) A token from [Hugging Face](https://huggingface.co/settings/tokens) for accessing sentence transformer models.

3.  **Launch everything with one command:**
    The `Makefile` makes this super easy. Just run:
    ```sh
    make up
    ```    This command will build the necessary Docker images and start all the services (the AI, the databases, etc.). It might take a few minutes the first time.

## API Endpoints

Once everything is running, you can interact with the system through its RESTful API, which will be available at `http://localhost:5555`.

Here's a guide to all the available endpoints:

---

### Agent Interaction

#### `POST /query`

This is the main endpoint to chat with the AI agent. Send your question, and the agent will use its tools (database, documents, web search) to find an answer.

*   **Request Body:**

    ```json
    {
      "query": "What was the total amount for invoice INV-2024-001?"
    }
    ```

*   **Success Response (200):**

    ```json
    {
      "result": "The total amount for invoice INV-2024-001 is 6000.00 MAD."
    }
    ```

---

### Document Management

#### `POST /upload`

Upload a file (PDF, DOCX, XLSX, TXT, etc.) to be processed and added to the AI's knowledge base.

*   **Request:** This is a `multipart/form-data` request. You would use a tool like Postman or a client library to upload a file under the `file` key.

*   **Success Response (200):**

    ```json
    {
      "filename": "my_invoice.pdf",
      "detail": "File processed and stored successfully."
    }
    ```

---

### Database Operations (PostgreSQL)

These endpoints interact directly with the structured accounting data in the PostgreSQL database.

#### `GET /invoices`

Fetches a list of all invoices from the `sage_invoices` table.

*   **Success Response (200):**

    ```json
    [
      {
        "id": 1,
        "invoice_number": "INV-2024-001",
        "contact_id": 1,
        "date": "2024-01-15",
        "due_date": "2024-02-15",
        "subtotal": "5000.00",
        "total_amount": "6000.00",
        "currency": "MAD",
        ...
      }
    ]
    ```

#### `GET /contacts`

Fetches a list of all contacts.

*   **Success Response (200):**

    ```json
    [
      {
        "id": 1,
        "name": "Mohamed Alami",
        "city": "Casablanca",
        "country": "Morocco",
        ...
      }
    ]
    ```

#### `GET /invoice_lines`

Fetches a list of all individual line items from all invoices.

*   **Success Response (200):**

    ```json
    [
      {
        "id": 1,
        "invoice_id": 1,
        "description": "Consulting hours - Strategy",
        "quantity": "20.00",
        "unit_price": "200.00",
        "total_amount": "4000.00",
        ...
      }
    ]
    ```

#### `POST /create_invoice`

Creates a new contact, a new invoice, and its associated line items in the database.

*   **Request Body:**

    ```json
    {
      "invoice_number": "INV-2025-101",
      "contact": {
        "name": "New Client Inc.",
        "address_line_1": "555 Tech Park",
        "city": "Innovate City",
        "postal_code": "12345",
        "country": "Techland"
      },
      "date": "2025-10-20",
      "due_date": "2025-11-20",
      "invoice_lines": [
        {
          "description": "Cloud Service Subscription",
          "quantity": 1,
          "unit_price": 300,
          "tax_amount": 60,
          "total_amount": 360
        },
        {
          "description": "Setup Fee",
          "quantity": 1,
          "unit_price": 150,
          "tax_amount": 30,
          "total_amount": 180
        }
      ],
      "subtotal": 450,
      "total_tax_amount": 90,
      "total_amount": 540,
      "currency": "USD"
    }
    ```

*   **Success Response (200):**

    ```json
    {
      "status": "success",
      "invoice_id": 11,
      "contact_id": 9
    }
    ```

---

### Debugging & Data Stores

These endpoints are useful for development and checking the state of the data stores.

#### `GET /chroma/all`

Retrieves all the document chunks and their metadata currently stored in the ChromaDB vector store.

#### `GET /mongo/all`

Retrieves all the raw document records from the MongoDB collection.

#### `DELETE /debug/erase-all`

**Use with caution!** This is a destructive operation that completely wipes all data from MongoDB and ChromaDB. It's useful for starting fresh without rebuilding the containers.

*   **Success Response (200):**

    ```
    "all documents erased successfully"
    ```

---

## Useful Makefile Commands

The `Makefile` has a few other handy commands:

*   `make down`: Stop and remove all the running containers.
*   `make logs`: View the logs from all services.
*   `make log_ai`: View the logs specifically from the AI service.
*   `make db_connect`: Connect directly to the PostgreSQL database to run your own SQL queries.
