from .arithmetic import arithmetic_execute
from .control_structures import control_structures_execute
from .data_structures import data_structures_execute
from .functions_and_pointers import functions_and_pointers_execute
from .error_handling import error_handling_execute
from .file_io import file_io_execute
from .gui import gui_execute
from .advanced_control_structures import advanced_control_structures_execute

def execute(command):
    # Convert command to lowercase for consistent keyword matching
    command = command.lower() 

    # Prioritize longer keywords to avoid false matches 
    keywords = [
        ("define function", functions_and_pointers_execute),
        ("create a pointer", functions_and_pointers_execute),
        ("write to file", file_io_execute),
        ("read from file", file_io_execute),
        ("create window", gui_execute),
        ("add button", gui_execute),
        ("start gui", gui_execute),
        ("add", arithmetic_execute),
        ("subtract", arithmetic_execute),
        ("multiply", arithmetic_execute),
        ("divide", arithmetic_execute),
        ("if", control_structures_execute),
        ("then", control_structures_execute),
        ("repeat", control_structures_execute),
        ("times", control_structures_execute),
        ("list", data_structures_execute),
        ("matrix", data_structures_execute),
        ("set", data_structures_execute),
        ("queue", data_structures_execute),
        ("stack", data_structures_execute),
        ("tree", data_structures_execute),
        ("try", error_handling_execute),
        ("except", error_handling_execute),
        ("while", advanced_control_structures_execute),
        ("switch", advanced_control_structures_execute),
        ("case", advanced_control_structures_execute),
        ("point", functions_and_pointers_execute)  # Add 'point' for pointer manipulation
    ]

    for keyword, func in keywords:
        if keyword in command:
            return func(command)

    return "I don't understand that command."