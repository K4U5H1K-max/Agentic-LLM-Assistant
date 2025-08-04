import os
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1")

def translate(text):
    match = re.search(r"'([^']+)'", text)
    phrase = match.group(1) if match else text
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "Translate the given English phrase into German."},
            {"role": "user", "content": phrase}
        ],
        temperature=0.5
    )
    return "Tool: " + response.choices[0].message.content.strip()
