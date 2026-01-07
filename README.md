# Question Bank Generator & Auditor

## Hackathon Submission

### Tech Stack

- **Frontend**: React + Vite + Tailwind + Lucide
- **Backend**: FastAPI + SQLModel + AsyncPG
- **AI**: LangChain + Ollama/LM Studio + pgvector

### Prerequisites

- Docker & Docker Compose
- Local LLM running (Ollama or LM Studio)
  - Default URL: `http://host.docker.internal:11434/v1` (Adjust in `backend/app/services/llm_service.py` or `.env` if needed)
  - Model: `llama3` (or adjust `LLM_MODEL`)

### How to Run

1. **Start the Application**

   ```bash
   docker-compose up --build
   ```

   This starts:

   - Postgres (DB + Vector Store) at port 5432
   - Backend API at port 8000

   _Note: Frontend is configured to run via `npm run dev` locally for better DX during hackathon, or can be dockerized._

2. **Start Frontend (Local)**

   ```bash
   cd frontend
   npm install
   npm run dev
   ```

   Access at `http://localhost:5173`

3. **Usage Flow**
   - Go to `http://localhost:5173`.
   - Create a Course (e.g., "Intro to AI").
   - Drag & Drop a PDF (Syllabus or Notes).
   - Go to Dashboard.
   - Enter a topic (e.g., "Transformers") and click "Generate".
   - Watch questions appear!

### Troubleshooting

- **DB Connection**: Ensure port 5432 is free.
- **LLM Connection**: If running Ollama on host, ensuring `host.docker.internal` works. If on Linux, use `--network host` or IP address.
