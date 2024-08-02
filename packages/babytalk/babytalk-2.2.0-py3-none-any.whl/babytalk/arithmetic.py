def arithmetic_execute(command):
    command = command.lower()  # Make it case-insensitive
    words = command.split()  # Split into words

    try:
        if "add" in words:
            num1_index = words.index("add") + 1
            num2_index = words.index("and") + 1
            return int(words[num1_index]) + int(words[num2_index])
        elif "subtract" in words:
            num1_index = words.index("subtract") + 1
            num2_index = words.index("from") + 1
            return int(words[num2_index]) - int(words[num1_index])
        elif "multiply" in words:
            num1_index = words.index("multiply") + 1
            num2_index = words.index("by") + 1
            return int(words[num1_index]) * int(words[num2_index])
        elif "divide" in words:
            num1_index = words.index("divide") + 1
            num2_index = words.index("by") + 1
            if int(words[num1_index]) == 0:
                return "Error: You can't divide by zero!"
            return int(words[num2_index]) / int(words[num1_index])
        else:
            return "I don't understand that arithmetic command."
    except (IndexError, ValueError):
        return "Please use a command like: 'add 5 and 3' or 'divide 10 by 2'."
