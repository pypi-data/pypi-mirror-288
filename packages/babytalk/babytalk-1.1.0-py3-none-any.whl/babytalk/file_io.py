def file_io_execute(command):
    if "write to file" in command:
        try:
            filename_start = command.index("write to file") + len("write to file") + 1
            content_start = command.index("content is") + len("content is") + 1
            filename = command[filename_start:content_start].strip()
            content = command[content_start:].strip()

            with open(filename, "w") as file:
                file.write(content)
            return f"Content written to {filename}."
        except Exception as e:
            return f"An error occurred: {e}"
        
    elif "read from file" in command:
        try:
            filename_start = command.index("read from file") + len("read from file") + 1
            filename = command[filename_start:].strip()
            
            with open(filename, "r") as file:
                content = file.read()
            return f"Content read from {filename}: {content}"
        except Exception as e:
            return f"An error occurred: {e}"
    
    else:
        return "I don't understand that file I/O command."
