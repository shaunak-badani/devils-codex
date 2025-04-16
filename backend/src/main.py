from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

app = FastAPI(root_path='/api')
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'agent'))
sys.path.append(PROJECT_ROOT)
from agent import DukeAgent

# list of allowed origins
origins = [
    "http://localhost:5173",
    "http://vcm-47087.vm.duke.edu"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello world!"}

@app.get("/chat")
def query_agent(query: str):
    """
    Query endpoint for the chatbot model
    Passes the query to the agent and returns the response
    """
    agent = DukeAgent()
    try:
        response_dictionary = agent.run(query)
        return response_dictionary
    except RuntimeError as e:
        raise HTTPException(status_code = 500, detail = str(e))
