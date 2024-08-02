def arithmetic_execute(command):
    try:
        parts = command.split()
        if "add" in command:
            return int(parts[1]) + int(parts[3])
        elif "subtract" in command:
            return int(parts[3]) - int(parts[1])
        elif "multiply" in command:
            return int(parts[1]) * int(parts[3])
        elif "divide" in command:
            return int(parts[3]) / int(parts[1])
        else:
            return "I don't understand that arithmetic command."
    except Exception as e:
        return f"Error during execution: {e}"
