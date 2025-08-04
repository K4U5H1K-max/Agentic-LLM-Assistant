import os
import re
from openai import OpenAI
from dotenv import load_dotenv
from calculator_tool import calculate
from translator_tool import translate

# Load environment and Groq API key
load_dotenv()
client = OpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1")

# LLM call
def ask_llm(prompt):
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def classify_task(part):
    part_lower = part.lower()
    if "translate" in part_lower:
        return "translation"
    elif any(op in part_lower for op in ["add", "plus", "multiply", "times", "*", "×"]):
        return "calculation"
    else:
        return "llm"

def detect_tasks(query):
    tasks = []

    calc_matches = re.findall(r'add\s+\d+\s+and\s+\d+|multiply\s+\d+\s+and\s+\d+', query, flags=re.IGNORECASE)
    for match in calc_matches:
        tasks.append(("calculation", match.strip()))

    trans_matches = re.findall(r"(translate\s+'[^']+')", query, flags=re.IGNORECASE)
    for match in trans_matches:
        tasks.append(("translation", match.strip()))

    cleaned_query = query
    for match in calc_matches + trans_matches:
        cleaned_query = cleaned_query.replace(match, "")

    leftover_parts = re.split(r'\bthen\b|,|\.|\band\b', cleaned_query, flags=re.IGNORECASE)
    for part in leftover_parts:
        part = part.strip()
        if part:
            task_type = classify_task(part)
            tasks.append((task_type, part))

    return tasks

# Logging
def log_interaction(user_input, responses):
    with open("interactions_level3.txt", "a", encoding="utf-8") as f:
        f.write(f"You: {user_input}\n")
        for step, response in enumerate(responses, start=1):
            f.write(f"Step {step}: {response}\n")
        f.write("\n")

# Main loop
def main():
    print("Agentic Smart Assistant (Level 3) — type 'exit' to quit")
    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() == "exit":
            break

        tasks = detect_tasks(user_input)
        responses = []

        for task_type, content in tasks:
            if task_type == "translation":
                result = translate(content)
                responses.append(f"Translation -> {result}")
            elif task_type == "calculation":
                result = calculate(content)
                responses.append(f"Calculation -> {result}")
            else:
                result = ask_llm(content)
                responses.append(f"Assistant -> {result}")

        for step, response in enumerate(responses, start=1):
            print(f"Step {step}: {response}")

        log_interaction(user_input, responses)

if __name__ == "__main__":
    main()