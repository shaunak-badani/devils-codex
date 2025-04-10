import os
from dotenv import load_dotenv
from openai import OpenAI
from tools.AIMengTools import AIMEngTools
import json
from executor import Executor


class DukeAgent:
    load_dotenv()
    client = OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))

    def __init__(self):
        self.messages = []

    def run(self, query):
        current_message = \
            {"role": "user", "content": query}
        self.messages.append(current_message)

        while True:
            response = self.client.responses.create(
                model="gpt-4o",
                input=self.messages,
                tools= AIMEngTools.TOOLS_SCHEMA,
                tool_choice="auto"
            )

            output = response.output[0]

            if output.type == "message":
                return output.content[0].text

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


    