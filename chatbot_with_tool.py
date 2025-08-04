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
            print("Goodbye!")
            break

        lower_input = user_input.lower()

        if lower_input.count("and") > 1 or (
            "and" in lower_input and any(kw in lower_input for kw in ["capital", "translate", "distance"])
        ):
            response = "Tool: Cannot handle multiple tasks at once."
            print(response)
            log_interaction(user_input, response)
        elif is_math_query(user_input):
            result = calculate(user_input)
            print(f"Tool: {result}")
            log_interaction(user_input, f"Tool: {result}")
        else:
            response = ask_llm(user_input)
            print(f"Assistant: {response}")
            log_interaction(user_input, f"Assistant: {response}")

def log_interaction(user_input, response):
    with open("interactions_level2.txt", "a") as log_file:
        log_file.write(f"User: {user_input}\n{response}\n\n")

if __name__ == "__main__":
    main()
