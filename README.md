# Accounting Assistance AI

Welcome to the Accounting Assistance AI project. This isn't your average, boring accounting software. Think of it as a smart helper that can chat with you about your financial documents, invoices, and even browse the web for information.

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
    Now, open up that new `.env` file and fill in your API keys (like for Google and Firecrawl).

3.  **Launch everything with one command:**
    The `Makefile` makes this super easy. Just run:
    ```sh
    make up
    ```    This command will build the necessary Docker images and start all the services (the AI, the databases, etc.).

## Usage

Once everything is up and running, the main way to interact with the project is through the API.

*   The AI service will be available at `http://localhost:5555`.

You can use tools like Postman or `curl` to send requests to the available endpoints. For example, to ask the AI a question:

```sh
curl -X POST "http://localhost:5555/query" \
     -H "Content-Type: application/json" \
     -d '{"query": "What was the total amount for invoice INV-2024-001?"}'
```

You can also upload documents, create new invoices, and fetch data directly from the databases. Check out `src/backend/routes.py` for all the available API endpoints.

### Useful Commands

The `Makefile` has a few other handy commands:

*   `make down`: Stop and remove all the running containers.
*   `make logs`: View the logs from all services.
*   `make log_ai`: View the logs specifically from the AI service.
*   `make db_connect`: Connect directly to the PostgreSQL database to run your own SQL queries.

## Features

*   **Natural Language Queries:** Ask questions about your financial data in plain English.
*   **Document Upload & Analysis:** Supports a wide range of document types, including PDFs, Word documents, and Excel spreadsheets.
*   **RAG (Retrieval-Augmented Generation):** The AI uses both your uploaded documents (from a ChromaDB vector store) and your structured database (PostgreSQL) to answer questions.
*   **Web Search Capabilities:** Can browse the web to find information that it doesn't have locally.
*   **RESTful API:** A clean and simple API for interacting with the system.
*   **Containerized:** Easy to set up and run thanks to Docker.

## Technologies Used

This project is built with a mix of modern and powerful tools:

*   **Backend:** Python, FastAPI
*   **AI/LLM:** Google Gemini, LangChain, Agno
*   **Databases:**
    *   **PostgreSQL:** For structured data like invoices and contacts.
    *   **MongoDB:** For storing the raw content of uploaded documents.
    *   **ChromaDB:** As a vector store for efficient similarity searches on document content.
*   **Containerization:** Docker, Docker Compose
*   **Web Scraping:** Firecrawl

---
