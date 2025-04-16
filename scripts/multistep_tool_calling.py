import openai
from openai import OpenAI
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os

load_dotenv()
# openai.api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))

# Step 1: Define your tools (functions)
tools = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "Gets the weather for a given location.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string"}
            },
            "required": ["location"]
        }
    },
    {
        "type": "function",
        "name": "suggest_outfit",
        "description": "Suggests an outfit based on the weather.",
        "parameters": {
            "type": "object",
            "properties": {
                "weather": {"type": "string"}
            },
            "required": ["weather"]
        }
    }
]


# Step 2: Simulated tool logic
def execute_tool(name, args):
    if name == "get_weather":
        location = args["location"]
        return f"The weather in {location} is sunny."
    elif name == "suggest_outfit":
        weather = args["weather"]
        if "sunny" in weather:
            return "Wear sunglasses and a t-shirt."
        elif "rainy" in weather:
            return "Bring an umbrella and wear boots."
    return "Unknown"

# Step 3: Begin the multi-step conversation
messages = [{"role": "user", "content": "What should I wear in New York tomorrow?"}]



while True:
    response = client.responses.create(
        model="gpt-4o",
        input=messages,
        tools=tools,
        tool_choice="auto"
    )

    output = response.output[0]

    if output.type == "message":
        print(f"Model output: {output.content[0].text}")
        break

    messages.append(output)  # Add LLM tool_call message
    name = output.name
    args = json.loads(output.arguments)
    result = execute_tool(name, args)
    print("Result : ", result)

    messages.append({
        "type": "function_call_output",
        "call_id": output.call_id,
        "output": result
    })



