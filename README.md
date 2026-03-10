# Agentic Research Assistant
This project is an AI-powered research agent capable of generating novel scientific hypotheses using Retrieval Augmented Generation (RAG).

## 📂 Project Structure

```
├── src/
│   ├── rag_engine/       # Member 1: Data & Retrieval
│   │   ├── db.py         # ChromaDB setup and ingestion
│   │   ├── retriever.py  # ArXiv paper fetching
│   │   └── verify_rag.py # RAG verification tests
│   ├── agent_core/       # Member 2: Logic & Reasoning
│   │   ├── graph.py      # LangGraph workflow
│   │   ├── nodes.py      # Agent nodes (retrieve, reason, hypothesize)
│   │   └── prompts.py    # System prompts
│   ├── formalizer/       # Member 3: Math & Reporting
│   │   ├── math_check.py # Mathematical validation
│   │   ├── critic.py     # Hypothesis critique
│   │   ├── report_generator.py # Markdown report generation
│   │   └── verify_formalizer.py # Formalizer tests
│   ├── api.py            # FastAPI server with SSE streaming
│   └── main.py           # CLI entry point
├── frontend/             # React + Vite UI
├── instructions/         # 📄 TEAM TASKS
│   ├── MEMBER_1_RAG.md
│   ├── MEMBER_2_AGENT.md
│   └── MEMBER_3_QUALITY.md
├── test_integration.py   # Full integration tests
├── requirements.txt
└── README.md
```

## 🚀 Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup Environment Variables

Copy `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
```

Edit `.env` and add at least one API key:
- **OpenAI**: For GPT-4 models (recommended)
- **Google**: For Gemini models (alternative)
- **Anthropic**: For Claude models (optional)

### 3. Run Tests

Test each member's work individually:

```bash
# Test Member 1 (RAG Engine)
cd src/rag_engine
python verify_rag.py

# Test Member 3 (Formalizer)
cd src/formalizer
python verify_formalizer.py

# Test full integration
python test_integration.py
```

### 4. Run the Application

**Option A: CLI Mode**
```bash
python src/main.py
```

**Option B: API Server**
```bash
python src/api.py
# Server runs on http://localhost:8000
```

**Option C: Full Stack (API + Frontend)**
```bash
# Terminal 1: Start backend
python src/api.py

# Terminal 2: Start frontend
cd frontend
npm install
npm run dev
```

## 🧠 Architecture

### Workflow
1. **Retrieve** → Searches ArXiv for relevant papers and stores in ChromaDB
2. **Reason** → Analyzes the topic and plans research approach
3. **Hypothesize** → Generates novel scientific hypothesis
4. **Critique** → Evaluates hypothesis quality and provides feedback
5. **Report** → Compiles everything into a formatted research paper

### Tech Stack
- **Database**: ChromaDB (Local Vector Store)
- **Orchestration**: LangGraph (Stateful agent workflow)
- **LLMs**: OpenAI GPT-4 / Google Gemini / Anthropic Claude
- **Backend**: FastAPI with Server-Sent Events
- **Frontend**: React + Vite + Tailwind CSS

## 🤝 Team Contributions

### Member 1: RAG Engine
- ArXiv paper retrieval
- ChromaDB vector storage
- Semantic search functionality

### Member 2: Agent Core
- LangGraph workflow design
- Agent nodes implementation
- Prompt engineering

### Member 3: Formalizer & Quality
- Mathematical validation
- Hypothesis critique system
- Report generation
- Integration testing

## 📝 Usage Examples

### CLI Example
```bash
$ python src/main.py
Enter your research topic/question: How can we optimize battery life in extreme cold?
[Agent] Starting research...
✓ Completed: retrieve
✓ Completed: reason
✓ Completed: hypothesize
✓ Completed: critique
✅ Report generated at: research_report_battery_optimization.md
```

### API Example
```bash
curl -X POST http://localhost:8000/api/research \
  -H "Content-Type: application/json" \
  -d '{"topic": "quantum computing applications"}'
```

## 🧪 Testing

Run the comprehensive test suite:
```bash
python test_integration.py
```

This tests:
- Member 1's RAG engine (ArXiv + ChromaDB)
- Member 2's agent workflow (LangGraph)
- Member 3's formalizer (Math + Critique + Reports)
- Full end-to-end integration

## 📚 API Documentation

Once the server is running, visit:
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/api/health

## 🔧 Configuration

### Switching LLM Providers

Edit `src/agent_core/nodes.py` to change the LLM:

```python
# OpenAI (default)
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

# Google Gemini
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)

# Anthropic Claude
from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0.7)
```

## 🐛 Troubleshooting

**ChromaDB Issues:**
```bash
# Clear the database
rm -rf chroma_db/
```

**API Rate Limits:**
- Add delays between requests
- Use lower-tier models for testing
- Check your API quota

**Import Errors:**
```bash
# Ensure src is in Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

## 📄 License

This project is for educational purposes.
