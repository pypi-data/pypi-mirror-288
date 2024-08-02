import tkinter as tk

def gui_execute(command):
    try:
        parts = command.split()
        
        # Create window
        if "create window called" in command:
            window_name = parts[-1]
            exec(f"global {window_name}; {window_name} = tk.Tk()")
            return f"Window {window_name} created."

        # Add button
        elif "add button called" in command:
            button_name = parts[-1]
            window_name = parts[-3]
            exec(f"global {button_name}; {button_name} = tk.Button({window_name}, text='{button_name}')")
            exec(f"{button_name}.pack()")
            return f"Button {button_name} added to {window_name}."

        # Start GUI
        elif "start gui" in command:
            window_name = parts[-1]
            exec(f"{window_name}.mainloop()")
            return "GUI started."

        else:
            return "I don't understand that GUI command."
    
    except Exception as e:
        return f"An error occurred: {e}"

# Example usage
print(gui_execute("create window called my_window"))
print(gui_execute("add button called my_button to my_window"))
print(gui_execute("start gui my_window"))
