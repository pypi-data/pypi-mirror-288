def control_structures_execute(command):
    command = command.lower()
    words = command.split()

    try:
        # Handle "if...do..."
        if "if" in words and "do" in words:
            condition_start = words.index("if") + 1
            condition_end = words.index("do")
            action = " ".join(words[condition_end + 1:])

            # Create a more Pythonic condition (add more translations if needed)
            condition_words = words[condition_start:condition_end]
            condition = " ".join(condition_words)
            condition = (
                condition.replace("is bigger than", ">")
                .replace("is smaller than", "<")
                .replace("is equal to", "==")
                .replace("and", "and")  # Handle 'and' in conditions
                .replace("or", "or")    # Handle 'or' in conditions
            )

            if eval(condition, globals()):
                exec(action, globals())
                return f"Yes, {condition}. So I did {action}."
            else:
                return f"No, {condition} is not true."

        # Handle "repeat...times..."
        elif "repeat" in words and "times" in words:
            times_index = words.index("repeat") + 1
            action_index = words.index("times") + 1

            # Check if the number of times is valid
            if not words[times_index].isdigit():
                return "Oops! Please tell me how many times to repeat using a number." 

            times = int(words[times_index])
            action = " ".join(words[action_index:])
            for _ in range(times):
                exec(action, globals())
            return f"I did {action} {times} times."

        else:
            return "I don't understand that."

    except (IndexError, ValueError) as e:
        return f"Oops! Something's wrong with your command. Try again."
