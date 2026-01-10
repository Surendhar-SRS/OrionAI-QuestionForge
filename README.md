
![Hero Banner](./docs/assets/question_forge_hero_1768048150385.png)

# 🛠️ Question Forge

**OrionAI-QuestionForge** is a cutting-edge, AI-powered platform designed to automate the generation, auditing, and refinement of high-quality academic assessments. By leveraging an **Agentic Multi-Step Workflow**, Question Forge transforms raw textbooks and course materials into structured, pedagogically sound questions in seconds.

---

## ✨ Key Features

- **🧠 Agentic Core**: A dual-agent system where a **Generator Agent** crafts questions and an **Auditor Agent** critiques them for quality and alignment.
- **📚 RAG-Powered Precision**: Ground every question in your specific source materials (PDF, Text, Markdown) to eliminate hallucinations.
- **🎨 Glassmorphic UI**: A premium, modern interface designed for a seamless and inspiring user experience.
- **✅ Bloom's Alignment**: Automatically map questions to cognitive levels (Recall, Analysis, Evaluation).
- **📦 LMS Ready**: One-click export to **QTI v2.1** (Canvas, Blackboard, Moodle) and professional **PDFs**.
- **🔐 Privacy First**: Support for **Local LLMs** (Ollama/Llama.cpp) ensuring your educational data never leaves your network.

---

## 🚀 Quick Start

### 1. Requirements

- **Docker & Docker Compose**
- **Node.js 18+**
- **Local LLM** (Ollama or LM Studio)

### 2. Launch Services

```bash
# Start Backend & Database
docker-compose up -d --build
```

### 3. Launch Frontend

```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173` to start forging!

---

## 📖 Deep Dive Documentation

For exhaustive technical specifications, operational guides, and architectural breakdowns, please refer to our full documentation:

👉 [**Full Project Documentation (Docs Folder)**](./docs/DOCUMENTATION.md)

---

## 🛠️ Built With

- **Frontend**: React 18, Vite, Tailwind CSS, Zustand, Recharts
- **Backend**: FastAPI, SQLModel, PostgreSQL + pgvector
- **AI**: LangChain, Pydantic AI, Instructor, Gemini 1.5 & Ollama
- **Desktop**: Electron

---

© 2026 OrionAI-QuestionForge | Redefining Assessment.
