# Scientific Agent Setup Guide

This guide explains how to set up the environment and run the Scientific Agent (Member 2).

## Prerequisites
- **Python 3.10+**: Ensure Python is installed and added to your system PATH.
  - Verify with: `python --version`

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

## Expected Output
The agent will simulate a reasoning process using the mock RAG tool and hypothesis generation using the mock Math tool. Output will be printed to the console showing the flow through the LangGraph nodes.
