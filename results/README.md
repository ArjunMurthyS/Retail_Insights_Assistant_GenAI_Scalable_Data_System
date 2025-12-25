# Retail Insights Assistant (GenAI + Scalable Data System)

## Overview
A scalable, GenAI-powered assistant capable of analyzing retail sales data using a Multi-Agent Architecture. The system supports natural language queries, handles large datasets via DuckDB (scalable to Cloud DW), and includes robust validation mechanisms.

## Features
- **Multi-Agent System**:
  - **Orchestrator**: Manages workflow.
  - **Planner**: Decomposes complex questions.
  - **Data Engineer**: Generates safe DuckDB SQL.
  - **Analyst**: Summarizes results into business insights.
  - **Validator**: Prevents SQL injection and Hallucinations.
## 💻 Cross-Platform Support (Windows / Mac / Linux)
This project is **platform-agnostic** thanks to Docker. It works identically on Windows, macOS, and Linux.

---

## 🚀 How to Run (3 Steps)

### 1. Prerequisites (Install First)
*   **Docker Desktop**: Download and install from [docker.com](https://www.docker.com/products/docker-desktop/).
    *   *Verify*: Open terminal and type `docker --version`.
*   **API Key**: You need an OpenAI API Key (preferred) or Google Gemini Key.

### 2. Configure Keys
1.  **Rename** `.env.example` to `.env`.
2.  **Edit** `.env` and paste your key:
    ```bash
    OPENAI_API_KEY=sk-proj-12345...
    ```

### 3. Start the App
Open a terminal in this folder and run:
```bash
docker-compose up --build
```
*(Note: On newer Docker versions, you can just use `docker compose up --build`)*

**Access the App:**
👉 **[http://localhost:8501](http://localhost:8501)**

---

## ❓ Troubleshooting

**Q: "Docker command not found"**
A: Ensure Docker Desktop is installed and running.

**Q: "Port 8501 already in use"**
A: Stop other containers using `docker ps` and `docker stop <id>`, or edit `docker-compose.yml` to change ports (e.g., `8502:8501`).

**Q: "API Key Error / Quota Exceeded"**
A: Check your `.env` file. Ensure there are no extra spaces. If using Gemini and you get 429 errors, switch to OpenAI.

**Q: "Container exits immediately"**
A: Run `docker logs <container_id>` to see the error. Usually it's a missing API key.

---

This project is fully self-contained. To run it on a new machine:

### 1. Configure Keys
1.  Rename `.env.example` to `.env`.
2.  Open `.env` and paste your API Key (OpenAI or Gemini).
    ```bash
    OPENAI_API_KEY=sk-proj-...
    ```

### 2. Start the App (Docker)
Run the following command in this folder:
```bash
docker-compose up --build
```
*(Ensure Docker Desktop is running)*

### 3. Use the App
Open your browser to:
👉 **[http://localhost:8501](http://localhost:8501)**

---

## 📋 Features & Capabilities
*   **Conversational Analytics**: "Compare Q1 and Q2 sales."
*   **Summarization**: "Give me a high-level summary."
*   **Robustness**: Self-healing API calls and SQL safety checks.
*   **Scalability**: Designed for 100GB+ workloads (see `presentation_slides.md`).

## 🛠️ Usage Guide

**1. Summarization Mode**
*   *Input*: "Summarize the sales performance for me."
*   *Action*: The agent will calculate total revenue, top products, and regional breakdown.

**2. Conversational Q&A Mode**
*   *Input*: "Which category had the highest revenue in March?"
*   *Input*: "Compare sales between Q1 and Q2."
*   *Action*: The Planner Agent will break down the request, the Data Engineer will run the SQL, and the Analyst will explain the findings.

## 📂 Project Structure
*   `src/`: Source code for Agents and Data Layer.
*   `Sales_Dataset/`: Place your `Amazon Sale Report.csv` here.
*   `tests/`: Unit and Hallucination tests.
*   `streamlit_app.py`: The Web UI entry point.
*   `docker-compose.yml`: Container orchestration.

## Docker Usage

Build and run everything in a container:
```bash
docker-compose up --build
```
This will mount your local code and data into the container and start the interactive shell.

## Testing
Run unit tests:
```bash
pytest tests
```

## Architecture
See [Architecture Docs](docs/architecture_scalability.md) for detailed design and scalability strategy.

## Technical Notes & Deliverables

### Setup & Execution Guide
1.  **Prerequisites**: Python 3.10+, pip.
2.  **Environment Setup**:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    ```
3.  **Run Application**:
    *   **CLI Mode**: `python src/sales_data_analysis/main.py --query "Summarize sales performance"`
    *   **Interactive Mode**: `python src/sales_data_analysis/main.py`
    *   **Streamlit UI**: `streamlit run streamlit_app.py`

### Assumptions
*   **Data**: The dataset is a structed CSV file (`Amazon Sale Report.csv`) located in `Sales_Dataset/`. The system assumes columns like `Date`, `Amount`, `Category`, `Region` exist or roughly maps to them.
*   **LLM**: The MVP uses simulated agent logic or basic LLM calls (OpenAI/Gemini) if configured. For local execution without API keys, fallback logic is used.
*   **Persistence**: `sales_data.db` (DuckDB/SQLite) is used for persistence.

### Limitations
*   **Context Window**: Extremely large result sets (thousands of rows) are truncated (top 50) before being passed to the LLM context to avoid token limits.
*   **Complex Joins**: The current CSV-to-SQL logic works best for single-table queries. Multi-table joins require expanded schema definitions.

### Improvements for Scale (100GB+)
To scale to 100GB+, we propose migration to a Data Lakehouse architecture:
1.  **Storage**: Migrate from local DuckDB file to **Snowflake** or **Delta Lake on S3**.
2.  **Compute**: Use **PySpark** for distributed data ingestion and aggregation.
3.  **Retrieval**: Implement **Vector Search (Pinecone)** for semantic product search to avoid full-text scans.
4.  **Orchestration**: Use **LangGraph** for more robust cyclic agent workflows (Planning <-> Execution).

See `architecture_presentation.md` in the `results/` folder for a detailed architectural breakdown.
