import os
from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from src.agent_core.prompts import RESEARCH_PLANNER_PROMPT, HYPOTHESIS_GENERATOR_PROMPT
from src.rag_engine.retriever import fetch_arxiv_papers
from src.rag_engine.db import ResearchDB

# Initialize DB
db = ResearchDB()

# Initialize LLM
# Note: In a real scenario, we'd handle different models here.
llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

def retrieval_node(state):
    """
    Fetches papers from ArXiv and ingests them into ChromaDB.
    Then retrieves the most relevant context.
    """
    topic = state["topic"]
    print(f"--- [Node: Retrieval] Searching for: {topic} ---")
    
    # 1. Fetch from ArXiv
    papers = fetch_arxiv_papers(topic, max_results=5)
    
    # 2. Ingest into DB
    db.ingest_papers(papers)
    
    # 3. Retrieve context (simulating the 'reading' phase)
    # We query with the topic itself to get the best matches
    context = db.search(topic, n_results=3)
    
    return {"context": context}

def reasoning_node(state):
    """
    Plans the research approach based on the topic.
    """
    topic = state["topic"]
    print(f"--- [Node: Reasoning] Planning for: {topic} ---")
    
    prompt = RESEARCH_PLANNER_PROMPT.format(topic=topic)
    response = llm.invoke([HumanMessage(content=prompt)])
    
    return {"reasoning_trace": response.content}

def hypothesis_node(state):
    """
    Generates the hypothesis using context and reasoning.
    """
    print(f"--- [Node: Hypothesis] Generating Hypothesis ---")
    topic = state["topic"]
    context_str = "\n\n".join(state["context"])
    reasoning = state["reasoning_trace"]
    
    prompt = HYPOTHESIS_GENERATOR_PROMPT.format(
        topic=topic,
        context=context_str,
        reasoning_trace=reasoning
    )
    
    response = llm.invoke([HumanMessage(content=prompt)])
    
    return {"hypothesis": response.content}
