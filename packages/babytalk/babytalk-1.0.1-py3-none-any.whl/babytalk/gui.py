import tkinter as tk

def gui_execute(command):
    try:
        parts = command.split()
        if "create window called" in command:
            window_name = parts[-1]
            exec(f"global {window_name}; {window_name} = tk.Tk()")
            return f"Window {window_name} created."
        elif "add button called" in command:
            button_name = parts[-1]
            window_name = parts[-3]
            exec(f"{button_name} = tk.Button({window_name}, text='{button_name}')")
            exec(f"{button_name}.pack()")
            return f"Button {button_name} added to {window_name}."
        elif "start gui" in command:
            window_name = parts[-1]
            exec(f"{window_name}.mainloop()")
            return "GUI started."
        else:
            return "I don't understand that GUI command."
    except Exception as e:
        return f"Error during execution: {e}"
