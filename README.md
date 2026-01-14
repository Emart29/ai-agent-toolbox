# 🤖 AI Agent Toolbox

A full-stack AI agent application with multiple tools including calculator, weather, web search, notes, and datetime utilities. Built with FastAPI backend and React frontend.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Node](https://img.shields.io/badge/node-18+-green.svg)

## ✨ Features

- **🧮 Calculator** - Mathematical operations and currency conversions
- **🌤️ Weather** - Real-time weather information via OpenWeatherMap
- **🔍 Web Search** - Internet search using Tavily/SerpAPI
- **📝 Notes** - Persistent note storage and retrieval
- **🕐 DateTime** - Time and date operations with timezone support
- **💬 Conversational AI** - Powered by Groq (Llama 3.3 70B)
- **🎨 Modern UI** - Clean, responsive React interface with Tailwind CSS

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+
- API Keys (see [Configuration](#configuration))

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/Emart29/ai-agent-toolbox.git
cd ai-agent-toolbox
```

**2. Run setup script**

**Windows:**
```bash
setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**3. Configure API keys**

Edit `backend/.env` and add your API keys:
```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
OPENWEATHER_API_KEY=your_openweather_key
# ... other keys
```

**4. Start the application**

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**5. Open your browser**

Visit: http://localhost:5173

## 📋 Configuration

### Required API Keys

1. **Groq API** (Required) - https://console.groq.com/keys
   - Free tier available
   - Used for LLM inference

2. **Tavily API** (Required) - https://tavily.com/
   - Free tier: 1000 searches/month
   - Primary web search provider

### Optional API Keys

3. **OpenWeatherMap** - https://openweathermap.org/api
   - Free tier: 1000 calls/day
   - For weather information

4. **Fixer.io** - https://fixer.io/
   - Free tier: 100 requests/month
   - For currency conversion

5. **SerpAPI** - https://serpapi.com/
   - Free tier: 100 searches/month
   - Fallback web search

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         React Frontend (Vite)           │
│  - Chat Interface                       │
│  - Real-time Updates                    │
│  - Responsive Design                    │
└─────────────────────────────────────────┘
                  ↕ HTTP/REST
┌─────────────────────────────────────────┐
│       FastAPI Backend Server            │
│  - RESTful API                          │
│  - CORS Middleware                      │
│  - Request Validation                   │
└─────────────────────────────────────────┘
                  ↕
┌─────────────────────────────────────────┐
│        AI Agent Orchestrator            │
│  - LangChain Integration                │
│  - Tool Selection                       │
│  - Response Generation                  │
└─────────────────────────────────────────┘
                  ↕
┌─────────────────────────────────────────┐
│            Tools Layer                  │
│  Calculator | Weather | Web Search     │
│  Notes | DateTime                       │
└─────────────────────────────────────────┘
```

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **LangChain** - AI agent framework
- **Groq** - LLM API (Llama 3.3 70B)
- **SQLAlchemy** - Database ORM
- **Uvicorn/Gunicorn** - ASGI server

### Frontend
- **React 19** - UI library
- **Vite** - Build tool
- **TanStack Query** - Data fetching
- **Tailwind CSS** - Styling
- **Radix UI** - Component primitives
- **Axios** - HTTP client

## 📖 Documentation

- [QUICKSTART.md](QUICKSTART.md) - 5-minute setup guide
- [deploy.md](deploy.md) - Deployment instructions

## 📦 Deployment

The application is ready to deploy to:

- ✅ Heroku
- ✅ Railway
- ✅ Google App Engine
- ✅ AWS EC2 / DigitalOcean VPS
- ✅ Vercel (frontend)
- ✅ Netlify (frontend)

See [deploy.md](deploy.md) for detailed instructions.

## 🔒 Security

- API keys stored in environment variables
- CORS configured for specific origins
- Input validation on all endpoints
- HTTPS ready for production
- Security headers configured

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Emmanuel Nwanguma**
- GitHub: [@Emart29](https://github.com/Emart29)
- LinkedIn: [Emmanuel Nwanguma](https://www.linkedin.com/in/nwangumaemmanuel)
- Email: nwangumaemmanuel29@gmail.com

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Backend framework
- [LangChain](https://python.langchain.com/) - AI agent framework
- [Groq](https://groq.com/) - LLM inference
- [Tailwind CSS](https://tailwindcss.com/) - Styling
- [Radix UI](https://www.radix-ui.com/) - UI components

---

**Built with ❤️ using FastAPI and React**
