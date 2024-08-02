def file_io_execute(command):
    command = command.lower()
    words = command.split()

    try:
        if "write" in words and "to file" in words:
            file_name = words[words.index("to") + 1]
            content_index = words.index("that") + 1  # Assuming "that" precedes the content
            content = " ".join(words[content_index:])

            with open(file_name, "w") as file:
                file.write(content)
            return f"Ok, I wrote '{content}' to the file {file_name}."

        elif "read from file" in words:
            file_name = words[words.index("from") + 1]

            with open(file_name, "r") as file:
                content = file.read()
            return f"I read this from {file_name}: {content}"

        else:
            return "I don't understand. Try saying 'write this to file <filename>' or 'read from file <filename>'."
    
    except FileNotFoundError:
        return "Oops! I couldn't find that file."
    except Exception as e:
        return f"Oops! Something went wrong: {e}"
