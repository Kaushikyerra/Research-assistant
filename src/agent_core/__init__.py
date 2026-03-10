"""
Agent Core Module - Member 2's Work
Handles LangGraph workflow and agent nodes.
"""

from .graph import build_graph, ResearchState
from .nodes import retrieval_node, reasoning_node, hypothesis_node
from .prompts import RESEARCH_PLANNER_PROMPT, HYPOTHESIS_GENERATOR_PROMPT

__all__ = [
    'build_graph',
    'ResearchState',
    'retrieval_node',
    'reasoning_node',
    'hypothesis_node',
    'RESEARCH_PLANNER_PROMPT',
    'HYPOTHESIS_GENERATOR_PROMPT'
]
