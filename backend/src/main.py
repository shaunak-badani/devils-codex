from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(root_path='/api')

# list of allowed origins
origins = [
    "http://localhost:5173",
    "http://vcm-45508.vm.duke.edu"
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
    """
    # Pass query to some function
    answer = f"I am a chatbot, still a work in progress!"
    # answer = f(query) 
    return {"answer": answer}