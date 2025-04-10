from openai import OpenAI
from dotenv import load_dotenv

import os

load_dotenv()
client = OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "developer",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "Are semicolons optional in JavaScript?"
        }
    ]
)

print(completion.choices[0])