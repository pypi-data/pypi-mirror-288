def control_structures_execute(command):
    parts = command.lower().split()
    
    # Handle "if" condition commands
    if "if" in parts and "then" in parts:
        try:
            condition = " ".join(parts[1:parts.index("then")])
            action = " ".join(parts[parts.index("then") + 1:])
            if eval(condition):
                exec(action)
                # Evaluate the result of the action if it returns a value
                return eval(action.split('(')[0] + '()')
        except Exception as e:
            return f"Error during execution: {e}"
        return "Condition met, action executed."

    # Handle "repeat" command
    elif "repeat" in parts and "times" in parts:
        try:
            times = int(parts[1])
            action = " ".join(parts[3:])
            for _ in range(times):
                exec(action)
            # Evaluate the result of the action if it returns a value
            return eval(action.split('(')[0] + '()')
        except Exception as e:
            return f"Error during execution: {e}"
        return f"Action repeated {times} times."

    else:
        return "I don't understand that control structure command."

# Example usage
print(control_structures_execute("if x > 10 then print('x is greater than 10')"))
print(control_structures_execute("repeat 3 times print('Hello')"))
