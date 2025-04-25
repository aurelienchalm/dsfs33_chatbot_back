from langchain.agents import initialize_agent
from langchain_openai import ChatOpenAI
from app.agent.tools import tools  # les outils customisés
import os

llm = ChatOpenAI(
    base_url="https://api.mistral.ai/v1",
    api_key=os.getenv("MISTRAL_API_KEY"),
    model="mistral-small-latest",
    temperature=0.7,
)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="chat-zero-shot-react-description",
    verbose=True,
    handle_parsing_errors=True,
)

async def run_agent(user_input: str) -> str:
    response = agent.run(user_input)
    return response