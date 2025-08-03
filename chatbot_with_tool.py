import os
import re
from dotenv import load_dotenv
from calculator_tool import calculate
from openai import OpenAI 

load_dotenv()
api_key = os.getenv("GROQ_API_KEY") 
client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)


def is_math_query(query):
    math_keywords = ["add", "plus", "subtract", "minus", "multiply", "times", "divide", "divided", "*", "/", "+", "-"]
    has_digits = bool(re.search(r'\d', query))
    has_keyword = any(word in query.lower() for word in math_keywords)
    return has_digits or has_keyword

def ask_llm(prompt):
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "system",
                "content": "Always think step-by-step and respond clearly and concisely."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response.choices[0].message.content.strip()

def main():
    print("Smart Assistant (Level 2) — type 'exit' to quit")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            break

        if is_math_query(user_input):
            result = calculate(user_input)
            print(f"Tool: {result}")
        elif "and" in user_input.lower() and any(op in user_input.lower() for op in ["add", "plus", "multiply", "*", "+", "times"]):
            print("Tool: Cannot handle multiple tasks at once.")
        else:
            response = ask_llm(user_input)
            print(f"Assistant: {response}")

if __name__ == "__main__":
    main()
