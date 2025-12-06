from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import os
from typing import Any, Dict

from agent.agentic_workflow import GraphBuilder

router = APIRouter()


class QueryRequest(BaseModel):
    query: str


@router.post("/query")
async def query_travel_agent(query: QueryRequest) -> Dict[str, Any]:
    """Handle incoming travel queries and return agent output as JSON.

    The GraphBuilder is created per-request. The `MODEL_PROVIDER` env var
    can be used to override the default provider (defaults to 'groq').
    """
    try:
        graph = GraphBuilder(model_provider=os.getenv("MODEL_PROVIDER", "groq"))
        react_app = graph()

        # Try to render a PNG of the internal graph (non-fatal)
        try:
            png_graph = react_app.get_graph().draw_mermaid_png()
            with open("my_graph.png", "wb") as f:
                f.write(png_graph)
        except Exception:
            # Don't fail the whole request if drawing fails (cloud environments
            # might not support binary drawing operations).
            pass

        # Invoke the agent with the incoming message(s)
        output = react_app.invoke({"messages": [query.query]})

        # Normalize the result into a string answer
        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content
        else:
            final_output = str(output)

        return {"answer": final_output}
    except Exception as e:
        # Raise an HTTP error so FastAPI returns a proper JSON error response
        raise HTTPException(status_code=500, detail=str(e))
