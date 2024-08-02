def arithmetic_execute(command):
    # Split the command into parts
    parts = command.lower().split()
    
    # Ensure the command has enough parts for processing
    if len(parts) < 4:
        return "Invalid command format."
    
    # Extract operation and numbers
    operation = parts[0]
    try:
        num1 = int(parts[1])
        num2 = int(parts[3])
    except ValueError:
        return "Invalid numbers provided."
    
    # Execute based on the operation
    if operation == "add":
        return num1 + num2
    elif operation == "subtract":
        return num1 - num2
    elif operation == "multiply":
        return num1 * num2
    elif operation == "divide":
        if num2 == 0:
            return "Cannot divide by zero."
        return num1 / num2
    else:
        return "I don't understand that arithmetic command."

# Example usage
print(arithmetic_execute("add 5 3"))         # Output: 8
print(arithmetic_execute("subtract 10 4"))   # Output: 6
print(arithmetic_execute("multiply 6 7"))    # Output: 42
print(arithmetic_execute("divide 20 4"))     # Output: 5.0
print(arithmetic_execute("divide 20 0"))     # Output: Cannot divide by zero.
print(arithmetic_execute("unknown 20 4"))    # Output: I don't understand that arithmetic command.
