
![Hero Banner](./docs/assets/question_forge_hero_1768048150385.png)

# 🛠️ Question Forge

**OrionAI-QuestionForge** is a cutting-edge, AI-powered platform designed to automate the generation, auditing, and refinement of high-quality academic assessments. By leveraging an **Agentic Multi-Step Workflow**, Question Forge transforms raw textbooks and course materials into structured, pedagogically sound questions in seconds.

---

## 🛡️ About the Project

**Question Forge** is a specialized solution for educators, institutions, and learners facing the "Assessment Bottleneck." Traditionally, creating high-quality exam questions is a labor-intensive process that requires deep pedagogical knowledge and significant time.

Our platform acts as an **Autonomous Co-pilot**, using a dual-agent system to not only generate content but critically audit it for academic rigor, factual grounding, and alignment with instructional goals. It aims to empower teachers to focus on student mentorship while the "Forge" handles the heavy lifting of content creation.

---

## 🌍 Socio-Economic Impact

Question Forge isn't just a tool; it's a driver for educational equity and institutional efficiency:

- **⚡ Eliminating Teacher Burnout**: Reduces the time required to create a comprehensive exam from hours to minutes, allowing educators to focus on 1-on-1 student mentorship.
- **� Democratizing High-Quality Education**: Provides under-resourced schools with the same advanced assessment-generation capabilities as elite institutions, free of charge.
- **📉 Cheating Prevention at Scale**: Enables the generation of unique, personalized exam sets for every student in a classroom, making traditional cheating practically impossible.
- **📊 Institutional ROI**: For large universities, the system can save thousands of man-hours annually, translating to millions in recovered productivity and higher instructional quality.

---

## �🚀 Key Features

- **🧠 Agentic Core**: A collaborative multi-agent loop where a **Generator Agent** crafts questions and an **Auditor Agent** provides real-time critiques and repair suggestions.
- **📚 RAG-Powered Precision**: Grounded in your own data; the AI "reads" your uploaded PDFs, notes, or textbooks via a vector database (pgvector) to ensure 100% factual accuracy.
- **🎨 Glassmorphic UI**: A premium, modern interface designed with React and Tailwind CSS for a seamless and inspiring professional workspace.
- **✅ Bloom's Alignment**: Automatically map questions to cognitive levels (Recall, Application, Analysis, Evaluation) and specific difficulty parameters.
- **📦 LMS & Print Ready**: One-click export to **QTI v2.1** (Canvas, Blackboard, Moodle) and professional, typeset **PDFs**.
- **🔐 Privacy First**: Native support for **Local LLMs** (via Ollama/Llama.cpp), ensuring sensitive academic documents never leave your local infrastructure.

---

## 💻 Technical Stack

- **Frontend**: React 18 (Vite), Tailwind CSS, Zustand (State Management), Recharts (Analytics).
- **Backend**: FastAPI (Asynchronous Python), SQLModel (ORM), PostgreSQL + pgvector (Vector Storage).
- **AI & Orchestration**: Pydantic AI, Instructor (Structured JSON Enforcement), LangChain.
- **LLM Support**: Gemini 1.5 Pro/Flash (Cloud) & Ollama (Local/Private).
- **Environment**: Electron (Desktop Wrapper), Docker & Docker Compose.

---

## 📖 Deep Dive Documentation

For exhaustive technical specifications, operational guides (10k+ words), and architectural breakdowns, please refer to our full documentation:

👉 [**Full Project Documentation (Docs Folder)**](./docs/DOCUMENTATION.md)

---

## ⚡ Quick Start

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

© 2026 OrionAI-QuestionForge | Redefining Assessment.
