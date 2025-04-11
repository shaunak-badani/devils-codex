from fastapi import FastAPI
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
def query_mean_model(query: str):
    """
    Query endpoint for the chatbot model
    Passes the query to the agent and returns the response
    """
    agent = DukeAgent()
    answer = agent.run(query)
    return {"answer": answer}