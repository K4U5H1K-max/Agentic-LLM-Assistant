import re

num_words = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
    "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
    "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
    "fourteen": 14, "fifteen": 15, "sixteen": 16,
    "seventeen": 17, "eighteen": 18, "nineteen": 19,
    "twenty": 20
}

def extract_numbers(query):
    query = query.lower()
    words = query.split()
    numbers = []

    for word in words:
        if word in num_words:
            numbers.append(num_words[word])
    digits = list(map(int, re.findall(r'\d+', query)))
    return numbers + digits

def calculate(query):
    query = query.lower()
    query = query.replace("x", "*").replace("×", "*")

    if re.fullmatch(r'[\d+\-*/().\s]+', query):
        try:
            return eval(query)
        except:
            return "Invalid expression"

    numbers = extract_numbers(query)

    if len(numbers) < 2:
        return "Need at least two numbers"

    if "add" in query or "plus" in query:
        return sum(numbers)
    elif "subtract" in query or "minus" in query:
        return numbers[0] - numbers[1]
    elif "multiply" in query or "times" in query:
        result = 1
        for num in numbers:
            result *= num
        return result
    elif "divide" in query or "divided" in query:
        try:
            return numbers[0] / numbers[1]
        except ZeroDivisionError:
            return "Cannot divide by zero"

    return "Unsupported operation"
