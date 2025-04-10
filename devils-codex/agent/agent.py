"""
Main LangGraph agent, defines state, nodes, graph flow
"""

import logging
from typing import Dict, List, Any, Optional, TypedDict

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, BaseMessage
from langchain_core.language_models import BaseLanguageModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

from langgraph.graph import StateGraph, END

from config import get_settings
from tool_config import Tools
from prompts import SYSTEM_PROMPT, TOOL_SELECTION_PROMPT, RESPONSE_SYNTHESIS_PROMPT
from memory import MemoryBuffer

from tools.aimengtool import AIMEngTool
from tools.eventstool import EventsTool
from tools.prospectivetool import ProspectiveTool
from tools.websearchtool import WebSearchTool
import os
from openai import OpenAI
import asyncio
import requests
import json

from tool_config import Weather


logger = logging.getLogger(__name__)



class DukeAgent:

    async def run(self, query):
        # query = What's the weather like in Paris today?
        memory = MemoryBuffer()
        input_messages = [{"role": "user", "content": "What's the weather like in Paris today?"}]
        memory.add_message("user", query)
        print("Memory messages: ", memory.load_messages())
        client = OpenAI(api_key = get_settings().OPENAI_API_KEY)
        response = client.responses.create(
            model="gpt-4o",
            input=memory.load_messages(),
            tools=Tools.get_tools()
        )
        

        tool_call = response.output[0]
        args = json.loads(tool_call.arguments)

        result = Weather.get_weather(args["latitude"], args["longitude"])
        print("Result : ", result)

        input_messages.append(tool_call)  # append model's function call message
        input_messages.append({                               # append result message
            "type": "function_call_output",
            "call_id": tool_call.call_id,
            "output": str(result)
        })

        response_2 = client.responses.create(
            model="gpt-4o",
            input=input_messages,
            tools=Tools.get_tools(),
        )
        return response_2.output_text
    


if __name__ == "__main__":
    agent = DukeAgent()
    while True:
        query = input("You: ")
        if query.lower() in {"exit", "quit"}:
            break
        response = asyncio.run(agent.run(query))
        print("Agent:", response)

