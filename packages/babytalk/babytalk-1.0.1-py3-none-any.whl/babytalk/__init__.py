from .arithmetic import arithmetic_execute
from .control_structures import control_structures_execute
from .data_structures import data_structures_execute
from .functions_and_pointers import functions_and_pointers_execute
from .error_handling import error_handling_execute
from .file_io import file_io_execute
from .gui import gui_execute
from .advanced_control_structures import advanced_control_structures_execute

def execute(command):
    if any(keyword in command for keyword in ["add", "subtract", "multiply", "divide"]):
        return arithmetic_execute(command)
    elif any(keyword in command for keyword in ["if", "then", "repeat", "times"]):
        return control_structures_execute(command)
    elif any(keyword in command for keyword in ["list", "matrix", "set", "queue", "stack", "tree"]):
        return data_structures_execute(command)
    elif any(keyword in command for keyword in ["define function", "create a pointer", "point"]):
        return functions_and_pointers_execute(command)
    elif "try" in command and "except" in command:
        return error_handling_execute(command)
    elif any(keyword in command for keyword in ["write to file", "read from file"]):
        return file_io_execute(command)
    elif any(keyword in command for keyword in ["create window", "add button", "start gui"]):
        return gui_execute(command)
    elif any(keyword in command for keyword in ["while", "switch", "case"]):
        return advanced_control_structures_execute(command)
    else:
        return "I don't understand that command."
