def advanced_control_structures_execute(command):
    command = command.lower()  # Ensure case-insensitivity

    # Handle "repeat" loop (simplified while loop)
    if command.startswith("repeat"):
        try:
            _, times_str, _, action = command.split(maxsplit=3)  # Extract components
            times = int(times_str)
            for _ in range(times):
                exec(action)
            return "Repeated the action."
        except Exception as e:
            return f"Error during 'repeat' execution: {e}"

    # Handle "check" and "do" (simplified switch-case)
    elif "check" in command and "do" in command:
        try:
            _, variable, _, *cases = command.split()
            for case in cases:
                if ":" not in case:  # Skip invalid cases
                    continue
                value, action = case.split(":")
                if eval(f"{variable} == {value}"):
                    exec(action)
                    return f"Checked {variable} and did the action for {value}."
            return f"Checked {variable}, but no match found."
        except Exception as e:
            return f"Error during 'check' execution: {e}"

    else:
        return "I don't understand that command."


# Example usage
x = 3
print(advanced_control_structures_execute("repeat 5 times: print('Hello!')"))
print(advanced_control_structures_execute("check x do 1: print('One') 2: print('Two') 3: print('Three')"))
