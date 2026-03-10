from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import json
import asyncio
from src.agent_core.graph import build_graph
from src.formalizer.report_generator import generate_markdown

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize graph once at startup
graph = build_graph()

class ResearchRequest(BaseModel):
    topic: str

@app.post("/api/research")
async def run_research(request: ResearchRequest):
    """
    Runs the research agent and streams events.
    Returns Server-Sent Events (SSE) stream.
    """
    async def event_generator():
        # Initialize state
        initial_state = {
            "topic": request.topic,
            "context": [],
            "reasoning_trace": "",
            "hypothesis": "",
            "feedback": "",
            "is_satisfactory": False,
            "revision_count": 0
        }
        
        print(f"[API] Starting research on: {request.topic}")
        
        try:
            # Accumulate state as we stream
            accumulated_state = initial_state.copy()
            
            # Stream events from the graph
            async for event in graph.astream(initial_state):
                # event is a dict where key is node name and value is the state update
                for node_name, state_update in event.items():
                    # Update accumulated state
                    accumulated_state.update(state_update)
                    
                    # Send progress update
                    data = {
                        "node": node_name,
                        "data": state_update,
                        "status": "processing"
                    }
                    yield f"data: {json.dumps(data)}\n\n"
                    await asyncio.sleep(0.1)  # Small buffer for client
            
            # Generate final report
            print("[API] Generating final report...")
            report = generate_markdown(accumulated_state)
            
            # Send completion with report
            completion_data = {
                "status": "complete",
                "report": report,
                "final_state": accumulated_state
            }
            yield f"data: {json.dumps(completion_data)}\n\n"
            
        except Exception as e:
            error_data = {
                "status": "error",
                "error": str(e)
            }
            yield f"data: {json.dumps(error_data)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.post("/api/report")
def create_report(state: dict):
    """
    Endpoint to generate markdown from state.
    Useful for regenerating reports from saved states.
    """
    try:
        report = generate_markdown(state)
        return {"report": report, "success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy", "version": "0.1"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
