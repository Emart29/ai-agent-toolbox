# 🤖 AI Agent Toolbox

> A full-stack conversational AI agent with real-world tool access — search the web, check the weather, run calculations, manage notes, and more. Built with a FastAPI backend and React frontend, powered by Llama 3.3 70B via Groq.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-19-61DAFB?style=flat-square&logo=react&logoColor=black)
![LangChain](https://img.shields.io/badge/LangChain-Agent-1C3C3C?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 📌 Overview

AI Agent Toolbox is a production-ready AI agent application that connects a conversational LLM to a suite of real-world tools. Rather than a static chatbot, the agent dynamically selects the right tool for each query — fetching live weather, performing currency conversions, searching the web, and persisting notes — all within a clean, responsive chat interface.

---

## ✨ Features

| Tool | Description |
|------|-------------|
| 🧮 **Calculator** | Mathematical operations and live currency conversions |
| 🌤️ **Weather** | Real-time weather data via OpenWeatherMap |
| 🔍 **Web Search** | Live internet search via Tavily / SerpAPI |
| 📝 **Notes** | Persistent note creation, retrieval, and management |
| 🕐 **DateTime** | Time, date, and timezone-aware operations |
| 💬 **Conversational AI** | Llama 3.3 70B via Groq — fast, capable, free-tier friendly |

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────┐
│                     React Frontend                        │
│          Chat UI · Real-time Updates · Tailwind CSS       │
└─────────────────────────┬────────────────────────────────┘
                          │  REST / HTTP
┌─────────────────────────▼────────────────────────────────┐
│                   FastAPI Backend                         │
│        RESTful API · CORS · Input Validation              │
└─────────────────────────┬────────────────────────────────┘
                          │
┌─────────────────────────▼────────────────────────────────┐
│              LangChain Agent Orchestrator                 │
│       Tool Selection · Reasoning · Response Generation    │
└──────┬──────────┬──────────┬──────────┬──────────┬───────┘
       │          │          │          │          │
   Calculator  Weather   Web Search   Notes   DateTime
```

---

## 🛠️ Tech Stack

**Backend**
- [FastAPI](https://fastapi.tiangolo.com/) — high-performance Python web framework
- [LangChain](https://python.langchain.com/) — agent orchestration and tool routing
- [Groq](https://console.groq.com/) — LLM inference (Llama 3.3 70B)
- [SQLAlchemy](https://www.sqlalchemy.org/) — database ORM for notes persistence
- [Uvicorn](https://www.uvicorn.org/) — ASGI server

**Frontend**
- [React 19](https://react.dev/) — UI library
- [Vite](https://vitejs.dev/) — fast build tooling
- [TanStack Query](https://tanstack.com/query) — async state and data fetching
- [Tailwind CSS](https://tailwindcss.com/) — utility-first styling
- [Radix UI](https://www.radix-ui.com/) — accessible component primitives
- [Axios](https://axios-http.com/) — HTTP client

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+
- API keys (see [Configuration](#-configuration))

### 1. Clone the repository

```bash
git clone https://github.com/Emart29/ai-agent-toolbox.git
cd ai-agent-toolbox
```

### 2. Run the setup script

```bash
# Linux / Mac
chmod +x setup.sh && ./setup.sh

# Windows
setup.bat
```

### 3. Add your API keys

```bash
# Edit backend/.env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
OPENWEATHER_API_KEY=your_openweather_key
```

### 4. Start the application

```bash
# Terminal 1 — Backend
cd backend
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows
uvicorn app.main:app --reload

# Terminal 2 — Frontend
cd frontend
npm run dev
```

### 5. Open in your browser

```
http://localhost:5173
```

---

## ⚙️ Configuration

### Required Keys

| Service | Purpose | Free Tier | Link |
|---------|---------|-----------|------|
| **Groq** | LLM inference | ✅ Available | [console.groq.com](https://console.groq.com/keys) |
| **Tavily** | Web search | ✅ 1,000 searches/mo | [tavily.com](https://tavily.com/) |

### Optional Keys

| Service | Purpose | Free Tier | Link |
|---------|---------|-----------|------|
| **OpenWeatherMap** | Weather data | ✅ 1,000 calls/day | [openweathermap.org](https://openweathermap.org/api) |
| **Fixer.io** | Currency conversion | ✅ 100 req/mo | [fixer.io](https://fixer.io/) |
| **SerpAPI** | Fallback web search | ✅ 100 searches/mo | [serpapi.com](https://serpapi.com/) |

---

## 📦 Deployment

The application is cloud-ready and can be deployed to any of the following:

| Platform | Frontend | Backend |
|----------|----------|---------|
| Vercel / Netlify | ✅ | — |
| Heroku / Railway | ✅ | ✅ |
| AWS EC2 / DigitalOcean | ✅ | ✅ |
| Google App Engine | ✅ | ✅ |

See [`deploy.md`](./deploy.md) for step-by-step instructions.

---

## 🔒 Security

- API keys managed via environment variables — never hardcoded
- CORS configured for specific, whitelisted origins
- Input validation enforced on all API endpoints
- Production-ready HTTPS and security header support

---

## 📄 License

This project is licensed under the [MIT License](./LICENSE).

---

## 👤 Author

**Emmanuel Nwanguma**

[![GitHub](https://img.shields.io/badge/GitHub-Emart29-181717?style=flat-square&logo=github)](https://github.com/Emart29)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/nwangumaemmanuel)
[![Email](https://img.shields.io/badge/Email-Contact-EA4335?style=flat-square&logo=gmail)](mailto:nwangumaemmanuel29@gmail.com)
