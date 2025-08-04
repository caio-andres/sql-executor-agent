from ..config.openai import client

response = client.responses.create(
    model="gpt-4.1", input="Write a one-sentence bedtime story about a unicorn."
)

if __name__ == "__main__":
    print(response.output_text)
