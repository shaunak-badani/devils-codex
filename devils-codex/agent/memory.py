from typing import List, Dict, Any
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

class MemoryBuffer:
    def __init__(self, max_turns: int = 10):
        self.max_turns = max_turns
        self.history: List[Dict[str, str]] = []

    def add_message(self, role: str, content: str):
        self.history.append({"role": role, "content": content})
        if len(self.history) > self.max_turns * 2:  # user + assistant per turn
            self.history = self.history[-self.max_turns * 2:]

    def load_messages(self) -> List[BaseMessage]:
        messages = []
        for m in self.history:
            if m["role"] == "user":
                messages.append(HumanMessage(content=m["content"]))
            elif m["role"] == "assistant":
                messages.append(AIMessage(content=m["content"]))
        return messages

    def clear(self):
        self.history = []

    def to_dict(self) -> List[Dict[str, str]]:
        return self.history
