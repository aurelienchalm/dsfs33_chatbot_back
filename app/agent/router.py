from fastapi import APIRouter
from pydantic import BaseModel
from app.agent.logic import run_agent

router = APIRouter()

class AgentRequest(BaseModel):
    user_input: str

class AgentResponse(BaseModel):
    answer: str

@router.post("/agent", response_model=AgentResponse)
async def agent_endpoint(request: AgentRequest):
    output = await run_agent(request.user_input)
    return AgentResponse(answer=output)