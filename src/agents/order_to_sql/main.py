from ...config.openai import client
from constants import SYSTEM_PROMPT, USER_PROMPT

response = client.responses.create(
    model="gpt-4.1", input="Write a one-sentence bedtime story about a unicorn."
)

completion = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "developer", "content": {SYSTEM_PROMPT}},
        {"role": "user", "content": {USER_PROMPT}},
    ],
)

if __name__ == "__main__":
    print(f"{client}\n\n\n\n")
    print(completion.choices[0].message)
