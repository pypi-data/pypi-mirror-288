def advanced_control_structures_execute(command):
    command = command.lower()
    words = command.split()

    try:
        # Handle "repeat until" loop
        if "repeat until" in command:
            condition_start = words.index("until") + 1
            action_start = words.index("repeat") + 2  
            condition = " ".join(words[condition_start:])
            action = " ".join(words[action_start:condition_start - 1])

            # Introduce a local namespace for safer variable handling
            local_vars = {}
            while not eval(condition, {}, local_vars):  # Repeat until condition is true
                exec(action, {}, local_vars)
            return "Finished repeating."

        # Handle "check" and "do" (simplified switch-case)
        elif "check" in words and "do" in words:
            variable = words[words.index("check") + 1]
            cases = command[command.index("do"):].split("do")

            for case in cases[1:]:
                case_parts = case.split(":")
                if len(case_parts) == 2:
                    case_value, action = case_parts
                    if variable.strip() == case_value.strip():
                        exec(action.strip(), globals())
                        return f"Checked {variable} and did {action}."
            return f"Checked {variable}, but nothing matched."

        else:
            return "I don't understand that."  # Generic error message

    except (IndexError, ValueError) as e:
        return "Oops! Something's wrong with your command. Try again."  # Simplified error for kids


# Example usage
x = 0
print(advanced_control_structures_execute("repeat until x is equal to 5 do x = x + 1"))
print(advanced_control_structures_execute("check x do 1: print('One') 2: print('Two') 5: print('Five')"))
