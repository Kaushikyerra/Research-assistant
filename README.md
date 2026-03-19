# Scientific Agent Setup Guide

This guide explains how to set up the environment and run the Scientific Agent (Member 2).

## Prerequisites
- **Python 3.10+**: Ensure Python is installed and added to your system PATH.
  - Verify with: `python --version`
- **Internet Connection**: Required to fetch real research papers from arXiv

## Setup Instructions

1.  **Install Dependencies**:
    Open a terminal in the project directory (`c:/Users/sathv/OneDrive/Documents/GEN_AI/`) and run:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure API Key**:
    - Open `.env` file.
    - Replace `your_api_key_here` with your actual Google API Key.
    - Save the file.

3.  **Verify Installation**:
    Ensure all packages are installed correctly.

## Running the Agent

To start the agent, run the main script:

```bash
python main.py
```

## Features

- **Real-time Literature Search**: Automatically fetches research papers from arXiv based on your query
- **AI-Powered Hypothesis Generation**: Uses Google Gemini to analyze papers and generate novel hypotheses
- **Iterative Refinement**: Critic agent evaluates and provides feedback for hypothesis improvement
- **Structured Output**: Generates comprehensive scientific proposals with problem statements, hypotheses, mathematical formulations, mechanisms, and next steps

## Expected Output
The agent will:
1. Search arXiv for relevant research papers based on your query
2. Analyze the retrieved papers using AI
3. Generate a structured scientific hypothesis
4. Evaluate and refine the hypothesis through critic feedback
5. Output a final comprehensive scientific proposal to the console
