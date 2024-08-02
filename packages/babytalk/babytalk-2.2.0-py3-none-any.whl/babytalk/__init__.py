from .arithmetic import arithmetic_execute
from .control_structures import control_structures_execute
from .data_structures import data_structures_execute
from .functions_and_pointers import functions_and_pointers_execute
from .error_handling import error_handling_execute
from .file_io import file_io_execute
from .gui import gui_execute
from .advanced_control_structures import advanced_control_structures_execute

def execute(command):
    command = command.lower()
    keywords = {
        "make a new action called": functions_and_pointers_execute,
        "write this to file": file_io_execute,
        "read from file": file_io_execute,
        "make a window named": gui_execute,
        "add a button to": gui_execute,
        "show the window": gui_execute,
        "add": arithmetic_execute,
        "subtract": arithmetic_execute,
        "multiply": arithmetic_execute,
        "divide": arithmetic_execute,
        "if": control_structures_execute,
        "repeat": control_structures_execute,
        "make a list named": data_structures_execute,
        "add to list": data_structures_execute,
        "make a set named": data_structures_execute,
        "add to set": data_structures_execute,
        "make a waiting line named": data_structures_execute,
        "add to waiting line": data_structures_execute,
        "next in line from": data_structures_execute,
        "make a tree named": data_structures_execute,
        "add to tree": data_structures_execute,  # Handle adding to tree
        "try this": error_handling_execute,
        "repeat until": advanced_control_structures_execute,  
        "check": advanced_control_structures_execute,
    }

    for keyword, func in keywords.items():  # Iterate over dictionary items
        if keyword in command:
            return func(command)

    return "I don't understand that command."
