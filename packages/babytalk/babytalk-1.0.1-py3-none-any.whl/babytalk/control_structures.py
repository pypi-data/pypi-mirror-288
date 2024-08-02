def control_structures_execute(command):
    try:
        parts = command.split()
        if "if" in command and "then" in command:
            condition = " ".join(parts[1:parts.index("then")])
            action = " ".join(parts[parts.index("then") + 1:])
            if eval(condition):
                exec(action)
                return eval(action.split('(')[0])
        elif "repeat" in command and "times" in command:
            times = int(parts[1])
            action = " ".join(parts[3:])
            for _ in range(times):
                exec(action)
            return eval(action.split('(')[0])
        else:
            return "I don't understand that control structure command."
    except Exception as e:
        return f"Error during execution: {e}"
