import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def build_prompt(user_input):
    if any(op in user_input for op in ['+', '-', '*', '/', 'add', 'subtract', 'multiply', 'divide']):
        return (
            f"User Question: {user_input}\n\n"
            "You are a helpful assistant. Refuse to perform arithmetic operations. "
            "Instead, suggest the user use a calculator."
        )
    else:
        return (
            f"User Question: {user_input}\n\n"
            "You are a helpful assistant. Think step-by-step and provide your answer in a clear, structured format. "
            "Use bullet points or numbered steps when helpful."
        )

def get_llm_response(prompt):
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Always think step-by-step and explain clearly."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    print("🔍 LLM Smart Assistant")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() == "exit":
            print("Goodbye!")
            break

        prompt = build_prompt(user_input)
        response = get_llm_response(prompt)

        print("\nAssistant:")
        print(response)
        print("\n")

        with open("interactions.txt", "a") as log_file:
            log_file.write(f"User: {user_input}\nAssistant: {response}\n\n")

if __name__ == "__main__":
    main()
