def functions_and_pointers_execute(command):
    command = command.lower()
    words = command.split()

    try:
        # Create a new action (function)
        if "make a new action called" in command:
            action_name = words[words.index("called") + 1]
            # Assume the rest of the command is the action to do
            action = " ".join(words[words.index("called") + 2:])

            # Define the function dynamically
            exec(f"def {action_name}(): {action}", globals())
            return f"Ok, I learned a new action called '{action_name}'."

        # Do the action (call the function)
        elif any(word in globals() for word in words):  # Check if any word is a defined action
            for word in words:
                if word in globals() and callable(globals()[word]):
                    globals()[word]()  # Call the function
                    return f"I did the '{word}' action."

        # Everything else is not understood yet
        else:
            return "I don't understand that. Try saying 'make a new action called...' or '<action_name>'."

    except Exception as e:
        return f"Oops! Something went wrong: {e}"
