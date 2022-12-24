import os
import openai
from dotenv import load_dotenv


load_dotenv()


openai.api_key = os.getenv("OPENAI_API_KEY")

prompt = input("Prompt: ")
response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=2048)
print(response.get('choices')[0]['text'])