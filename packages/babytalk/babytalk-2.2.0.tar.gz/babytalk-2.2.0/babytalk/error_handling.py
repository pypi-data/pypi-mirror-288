def error_handling_execute(command):
    command = command.lower()
    words = command.split()

    try:
        if "try this" in command and "if error do this" in command:
            try_start = words.index("try") + 2  # Start after "try this"
            except_start = words.index("if")  # Start at "if" of "if error do this"
            
            try_block = " ".join(words[try_start:except_start])
            except_block = " ".join(words[except_start + 3:]) # Start after "if error do this"

            try:
                exec(try_block, globals())
                return "Tried it and it worked!"
            except Exception as e:
                exec(except_block, globals())
                # Provide more specific feedback about the error
                return f"Oops, there was an error: {e}. So I did {except_block} instead." 
        else:
            return "I don't understand that. Try saying 'try this... if error do this...'"
    except (IndexError, ValueError) as e:
        return "Oops! Something's wrong with your command. Try again."
