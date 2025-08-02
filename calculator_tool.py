import re

def calculate(query):
    query = query.lower()

    numbers = list(map(int, re.findall(r'\d+', query)))

    if "add" in query or "plus" in query:
        return sum(numbers)

    elif "subtract" in query or "minus" in query:
        return numbers[0] - numbers[1] if len(numbers) >= 2 else "Need two numbers"

    elif "multiply" in query or "times" in query:
        result = 1
        for num in numbers:
            result *= num
        return result

    elif "divide" in query or "divided" in query:
        try:
            return numbers[0] / numbers[1]
        except (ZeroDivisionError, IndexError):
            return "Invalid division"

    else:
        return "Unsupported operation"
