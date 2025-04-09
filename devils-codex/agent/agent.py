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
from prompts import SYSTEM_PROMPT, TOOL_SELECTION_PROMPT, RESPONSE_SYNTHESIS_PROMPT
from memory import MemoryBuffer

from tools.aimengtool import AIMEngTool
from tools.eventstool import EventsTool
from tools.prospectivetool import ProspectiveTool
from tools.websearchtool import WebSearchTool

import asyncio

logger = logging.getLogger(__name__)

class AgentState(TypedDict):
    messages: List[BaseMessage]
    selected_tool: Optional[str]
    tool_output: Optional[str]
    conversation_id: Optional[str]
    user_id: Optional[str]


def get_llm() -> BaseLanguageModel:
    settings = get_settings()
    return ChatOpenAI(
        model=settings.MODEL_NAME,
        openai_api_key=settings.OPENAI_API_KEY,
        temperature=0.2
    )


def planner_node(state: AgentState) -> Dict[str, Any]:
    llm = get_llm()
    query = state['messages'][-1].content

    planner_prompt = TOOL_SELECTION_PROMPT.format(query=query)

    messages = [
        SystemMessage(content=SYSTEM_PROMPT), 
        SystemMessage(content=planner_prompt),
        HumanMessage(content=query)
    ]

    response = llm.invoke(messages).content.strip()
    # valid_tools = {"ai_meng_tool", "events_tool", "prospective_tool", "web_search_tool"}
    valid_tools = {"ai_meng_tool", "web_search_tool"}
    selected = response if response in valid_tools else "web_search_tool"
    return {**state, "selected_tool": selected}


def tool_router_node(state: AgentState) -> Dict[str, Any]:
    tool_name = state["selected_tool"]
    question = state['messages'][-1].content

    tool_map = {
        "ai_meng_tool": AIMEngTool(),
        # "events_tool": EventsTool(),
        # "prospective_tool": ProspectiveTool(),
        "web_search_tool": WebSearchTool()
    }

    tool = tool_map[tool_name]
    output = tool.run(question)
    return {**state, "tool_output": output}


def final_response_node(state: AgentState) -> Dict[str, Any]:
    llm = get_llm()
    query = state["messages"][-1].content
    search_results = state["tool_output"]

    prompt = RESPONSE_SYNTHESIS_PROMPT.format(
        query=query, 
        # tool_results=state["tool_output"],
        tool_results=search_results
    )

    messages = [SystemMessage(content=prompt)]
    response = llm.invoke(messages).content.strip()

    return {
        "messages": state["messages"] + [AIMessage(content=response)],
        "tool_output": state["tool_output"],
        "selected_tool": state["selected_tool"],
        "conversation_id": state["conversation_id"],
        "user_id": state["user_id"]
    }


class DukeAgent:
    def __init__(self):
        self.memory = MemoryBuffer()
        self.graph = self._build_graph()

    def _build_graph(self):
        graph = StateGraph(AgentState)
        graph.add_node("planner", planner_node)
        graph.add_node("tool_router", tool_router_node)
        graph.add_node("final", final_response_node)

        graph.set_entry_point("planner")
        graph.add_edge("planner", "tool_router")
        graph.add_edge("tool_router", "final")
        graph.add_edge("final", END)

        return graph.compile()

    async def run(self, message: str, conversation_id=None, user_id=None) -> str:
        self.memory.add_message("user", message)
        messages = self.memory.load_messages()

        state = AgentState(
            messages=messages,
            selected_tool=None,
            tool_output=None,
            conversation_id=conversation_id,
            user_id=user_id
        )

        # Await the asynchronous call
        result = await self.graph.ainvoke(state)

        final_msg = next((m for m in result["messages"] if isinstance(m, AIMessage)), None)

        if final_msg:
            self.memory.add_message("assistant", final_msg.content)
            return final_msg.content
        else:
            return "Sorry, I couldn't process that."


def get_agent() -> DukeAgent:
    global _agent_instance
    if '_agent_instance' not in globals():
        _agent_instance = DukeAgent()
    return _agent_instance


if __name__ == "__main__":
    agent = DukeAgent()
    while True:
        query = input("You: ")
        if query.lower() in {"exit", "quit"}:
            break
        response = asyncio.run(agent.run(query))
        print("Agent:", response)

