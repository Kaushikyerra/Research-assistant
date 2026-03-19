import operator
import os
import json
import ast
from typing import Annotated, Sequence, TypedDict, Union, Literal
from dotenv import load_dotenv

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

# Import mock tools
from rag_engine import RAGEngine
from math_tools import MathTools
from mock_critic import MockCritic

# Initialize tools
rag = RAGEngine()
math_tools = MathTools()
critic_tool = MockCritic()

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-flash-latest")

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    research_data: str
    hypothesis: str
    critique_feedback: str
    revision_count: int

import time

def extract_text(content) -> str:
    # If the content is a string that looks like a dictionary or list, try parsing it
    if isinstance(content, str) and (content.strip().startswith("{") or content.strip().startswith("[")):
        try:
            parsed = ast.literal_eval(content.strip())
            content = parsed
        except (ValueError, SyntaxError):
            pass # Fall back to treating it as just a string
            
    if isinstance(content, str):
        return content.strip()
    elif isinstance(content, list):
        return " ".join([part.get("text", "") if isinstance(part, dict) else str(part) for part in content]).strip()
    elif isinstance(content, dict) and 'text' in content:
        return content['text'].strip()
    else:
        return str(content).strip()

def invoke_with_retries(chain, inputs, max_retries=5, initial_wait=15):
    """
    Wraps LangChain invoke calls with exponential backoff retries 
    to handle Gemini API free-tier rate limits gracefully.
    """
    wait_time = initial_wait
    for attempt in range(max_retries):
        try:
            return chain.invoke(inputs)
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                if attempt == max_retries - 1:
                    print("[Rate Limit] Max retries exhausted. Failing.")
                    raise
                print(f"[Rate Limit] Hit 429 Quota Exhausted. Waiting {wait_time} seconds before retrying (Attempt {attempt + 1}/{max_retries})...")
                time.sleep(wait_time)
                wait_time *= 2  # Exponential backoff
            else:
                raise

def reasoning_node(state: AgentState):
    """
    Module 1: Reasoning Node
    Analyzes the user problem and gathers initial research data.
    """
    print("--- REASONING NODE ---")
    messages = state['messages']
    last_message = messages[-1]
    
    # Use LLM to analyze the reason prompt and decide what to search for
    prompt = ChatPromptTemplate.from_template(
        """Analyze the following user problem and generate a SHORT, CONCISE search query (maximum 10 words) for arXiv scientific literature.

User Problem: {input}

Return ONLY the search keywords, nothing else. Example format: "battery optimization cold temperature lithium ion"
"""
    )
    chain = prompt | llm
    response = invoke_with_retries(chain, {"input": last_message.content})
    
    # Handle generic content type
    query = extract_text(response.content)
    
    # Ensure query is short enough for arXiv API
    if len(query) > 200:
        # Extract key terms if query is too long
        words = query.split()[:10]
        query = " ".join(words)
        
    print(f"Generated Search Query: {query}")
    
    # Call Member 1's tool
    research_results = rag.search_literature(query)

    # Slow down requests to avoid 429 errors from Google Gemini Free Tier
    print("Pausing execution for 15s to respect API Rate Limits...")
    time.sleep(15)
    
    return {"research_data": research_results, "messages": [AIMessage(content=f"Analyzed problem. Query: {query}")]}

def hypothesis_node(state: AgentState):
    """
    Module 3: Hypothesis Node
    Generates a novel scientific hypothesis based on research data.
    """
    print("--- HYPOTHESIS NODE ---")
    research_data = state.get('research_data', '')
    user_problem = state['messages'][0].content
    critique = state.get('critique_feedback', None)
    
    prompt_text = r"""
    Based on the following research data regarding '{problem}', generate a comprehensive and structured scientific proposal.
    
    Research Data:
    {data}
    
    Your output MUST include the following structured sections:
    1. **Problem Statement**: Clearly define the problem based on the user's query.
    2. **Hypothesis**: Provide a unique and novel scientific hypothesis (not just summarizing data).
    3. **Mathematical Formulations**: Include governing equations. IMPORTANT: Do NOT use raw LaTeX blocks or unrendered math syntax (e.g. no `$$`, no `\eta`). Please formulate your math clearly using plain readable text or Unicode symbols (e.g. use "Viscosity (n)" instead of "\eta", "e^(...)" instead of "\exp"). Make it extremely readable for a simple terminal output.
    4. **Proposed Mechanism**: Detail exactly how the proposed system/solution works.
    5. **Way Forward**: Suggest concrete next steps, experiments, or validations to test this hypothesis.
    """
    
    if critique:
        print(f"--- REFINING HYPOTHESIS (Feedback: {critique}) ---")
        prompt_text += f"\nCRITIC FEEDBACK TO ADDRESS: {critique}\nEnsure you fix the issues raised."
    
    prompt = ChatPromptTemplate.from_template(prompt_text)
    chain = prompt | llm
    response = invoke_with_retries(chain, {"problem": user_problem, "data": research_data})
    
    # Handle generic content type
    hypothesis = extract_text(response.content)

    # Call Member 3's tool to check formal validity
    check_result = math_tools.check_equations(hypothesis)
    
    final_hypothesis = f"{hypothesis}\n\nValidation: {check_result}"
    
    # Slow down requests to avoid 429 errors from Google Gemini Free Tier
    print("Pausing execution for 15s to respect API Rate Limits...")
    time.sleep(15)
    
    return {"hypothesis": final_hypothesis, "messages": [AIMessage(content="Generated hypothesis.")]}

def critic_node(state: AgentState):
    """
    Module 3 (Critic): Evaluates the hypothesis.
    """
    print("--- CRITIC NODE ---")
    hypothesis = state['hypothesis']
    
    # Call Mock Critic
    evaluation = critic_tool.evaluate(hypothesis)
    
    score = evaluation['score']
    feedback = evaluation['feedback']
    
    print(f"Critic Score: {score}")
    print(f"Critic Feedback: {feedback}")
    
    # Increment revision count
    current_revisions = state.get('revision_count', 0)
    
    return {
        "critique_feedback": feedback,
        "revision_count": current_revisions + 1
    }

def check_critique(state: AgentState) -> Literal["hypothesis", END]:
    """
    Conditional edge to determine next step based on critique.
    """
    critique = state.get('critique_feedback', "")
    revision_count = state.get('revision_count', 0)
    
    # Basic logic: If feedback contains "Approved", we pass.
    # In a real system, we'd use the score.
    if "Approved" in critique:
        print("--- CRITIC PASSED ---")
        return END
    
    if revision_count >= 3:
        print("--- MAX REVISIONS REACHED ---")
        return END
        
    print("--- CRITIC REJECTED -> LOOPING BACK ---")
    return "hypothesis"

# Define the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("reasoning", reasoning_node)
workflow.add_node("hypothesis", hypothesis_node)
workflow.add_node("critic", critic_node)

# Set entry point
workflow.set_entry_point("reasoning")

# Add edges
workflow.add_edge("reasoning", "hypothesis")
workflow.add_edge("hypothesis", "critic")

# Add conditional edge from critic
workflow.add_conditional_edges(
    "critic",
    check_critique
)

# Compile the graph
app = workflow.compile()
