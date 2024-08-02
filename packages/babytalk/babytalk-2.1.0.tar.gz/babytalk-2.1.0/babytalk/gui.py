import tkinter as tk

def gui_execute(command):
    command = command.lower()
    words = command.split()

    try:
        if "make a window named" in command:
            window_name = words[-1]
            globals()[window_name] = tk.Tk()
            return f"Ok, I made a window named {window_name}."

        elif "add a button to" in command and "that says" in command:
            window_name = words[words.index("to") + 1]
            button_text = " ".join(words[words.index("says") + 1:])
            button_name = f"button_{button_text.replace(' ', '_')}"  # Create unique button name

            globals()[button_name] = tk.Button(globals()[window_name], text=button_text)
            globals()[button_name].pack()

            return f"I added a button to {window_name} that says '{button_text}'."

        elif "show the window" in command:
            window_name = words[-1]
            globals()[window_name].mainloop()
            return f"Showing the window {window_name}."

        else:
            return "I don't understand. Try saying 'make a window named...', 'add a button to... that says...', or 'show the window...'"

    except (IndexError, KeyError, tk.TclError) as e:
        return f"Oops! Something went wrong: {e}"
