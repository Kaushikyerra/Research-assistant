# Quick Start Guide

Get the Agentic Research Assistant running in 5 minutes!

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- An API key from OpenAI, Google, or Anthropic

## Step 1: Clone and Setup (1 min)

```bash
# Navigate to project directory
cd Research-assistant

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Configure API Key (1 min)

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your API key
# For OpenAI:
OPENAI_API_KEY=sk-proj-your-key-here

# OR for Google Gemini:
GOOGLE_API_KEY=your-google-key-here
```

## Step 3: Test the System (2 min)

```bash
# Run integration tests
python test_integration.py
```

Expected output:
```
✅ Member 1 (RAG): PASSED
✅ Member 2 (Agent): PASSED
✅ Member 3 (Formalizer): PASSED
✅ Full Integration: PASSED
```

## Step 4: Run Your First Research (1 min)

```bash
# Start the CLI
python src/main.py
```

When prompted, enter a research topic:
```
Enter your research topic/question: How can AI improve drug discovery?
```

The agent will:
1. Search ArXiv for relevant papers
2. Analyze the literature
3. Generate a novel hypothesis
4. Critique the hypothesis
5. Create a research report

## What You Get

A markdown file like `research_report_AI_drug_discovery.md` containing:
- Abstract
- Literature context
- Reasoning process
- Novel hypothesis
- Critical evaluation

## Next Steps

### Run the API Server
```bash
python src/api.py
# Visit http://localhost:8000/docs for API documentation
```

### Run the Frontend
```bash
cd frontend
npm install
npm run dev
# Visit http://localhost:5173
```

### Customize the Agent

Edit these files to modify behavior:
- `src/agent_core/prompts.py` - Change how the agent thinks
- `src/agent_core/nodes.py` - Modify the workflow
- `src/formalizer/critic.py` - Adjust critique criteria

## Troubleshooting

### "No module named 'src'"
```bash
# Add src to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### "API key not found"
Make sure your `.env` file is in the project root and contains a valid API key.

### "ChromaDB error"
```bash
# Clear the database and try again
rm -rf chroma_db/
```

### Rate Limit Errors
- Wait a few minutes between runs
- Use a lower-tier model (e.g., gpt-3.5-turbo instead of gpt-4)
- Check your API quota

## Example Topics to Try

- "How can we improve solar panel efficiency?"
- "What are novel approaches to carbon capture?"
- "How can quantum computing accelerate machine learning?"
- "What are new methods for early cancer detection?"
- "How can we optimize battery life in extreme temperatures?"

## Support

For issues or questions:
1. Check the main README.md
2. Review the instructions/ folder for detailed documentation
3. Run the test suite to identify which component has issues

Happy researching! 🧪🔬
