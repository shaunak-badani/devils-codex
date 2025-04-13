import os
from dotenv import load_dotenv
from openai import OpenAI, RateLimitError
from tools.AIMengTools import AIMEngTools
from tools.ProspectiveStudentsTool import ProspectiveStudentsTool
from tools.EventTools import EventTools
import json
from executor import Executor
import time


class DukeAgent:
    load_dotenv()
    client = OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))

    def __init__(self):
        self.messages = []

    def get_tools(self):
        return [
            *AIMEngTools.TOOLS_SCHEMA,
            *ProspectiveStudentsTool.TOOLS_SCHEMA,
            *EventTools.TOOLS_SCHEMA
        ]

    def run(self, query):
        current_message = \
            {"role": "user", "content": query}
        self.messages.append(current_message)
        start = time.time()
        while True:
            try:
                response = self.client.responses.create(
                    model="gpt-4o-mini",
                    input=self.messages,
                    tools=self.get_tools(),
                    tool_choice="auto"
                )
            except RateLimitError:
                raise RuntimeError("Cannot run the query due to rate limits. Please wait for a few seconds and try again later.")


            output = response.output[0]

            if output.type == "message":
                end = time.time()
                total_time = end - start
                return {
                    "time": f"{total_time:.6f} s",
                    "answer": output.content[0].text
                }
            print("Output :", output)
            self.messages.append(output)  # Add LLM tool_call message
            name = output.name
            args = json.loads(output.arguments)
            result = Executor.execute_tool(name, args)
            print("Result : ", result)

            self.messages.append({
                "type": "function_call_output",
                "call_id": output.call_id,
                "output": str(result)
            })


if __name__ == "__main__":
    agent = DukeAgent()
    while True:
        query = input("You: ")
        if query.lower() in {"exit", "quit"}:
            break
        response = agent.run(query)
        print("Agent:", response)


    