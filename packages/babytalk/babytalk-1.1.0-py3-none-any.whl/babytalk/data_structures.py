from collections import deque

def data_structures_execute(command):
    parts = command.split()
    
    # Lists and Matrices
    if "create a list called" in command:
        list_name = parts[-1]
        globals()[list_name] = []
        return f"List {list_name} created."
    elif "add" in command and "to list" in command:
        item = parts[1]
        list_name = parts[4]
        if list_name in globals():
            globals()[list_name].append(item)
            return f"Added {item} to {list_name}."
        else:
            return f"List {list_name} does not exist."
    elif "create a matrix called" in command:
        matrix_name = parts[-1]
        globals()[matrix_name] = []
        return f"Matrix {matrix_name} created."
    elif "add row" in command and "to matrix" in command:
        row = eval(parts[2])
        matrix_name = parts[-1]
        if matrix_name in globals():
            globals()[matrix_name].append(row)
            return f"Added row {row} to {matrix_name}."
        else:
            return f"Matrix {matrix_name} does not exist."
    
    # Sets
    elif "create a set called" in command:
        set_name = parts[-1]
        globals()[set_name] = set()
        return f"Set {set_name} created."
    elif "add" in command and "to set" in command:
        item = parts[1]
        set_name = parts[4]
        if set_name in globals():
            globals()[set_name].add(item)
            return f"Added {item} to {set_name}."
        else:
            return f"Set {set_name} does not exist."
    
    # Queues
    elif "create a queue called" in command:
        queue_name = parts[-1]
        globals()[queue_name] = deque()
        return f"Queue {queue_name} created."
    elif "enqueue" in command and "to queue" in command:
        item = parts[1]
        queue_name = parts[4]
        if queue_name in globals():
            globals()[queue_name].append(item)
            return f"Enqueued {item} to {queue_name}."
        else:
            return f"Queue {queue_name} does not exist."
    elif "dequeue from queue" in command:
        queue_name = parts[-1]
        if queue_name in globals() and globals()[queue_name]:
            item = globals()[queue_name].popleft()
            return f"Dequeued {item} from {queue_name}."
        else:
            return f"Queue {queue_name} does not exist or is empty."
    
    # Stacks
    elif "create a stack called" in command:
        stack_name = parts[-1]
        globals()[stack_name] = []
        return f"Stack {stack_name} created."
    elif "push" in command and "to stack" in command:
        item = parts[1]
        stack_name = parts[4]
        if stack_name in globals():
            globals()[stack_name].append(item)
            return f"Pushed {item} to {stack_name}."
        else:
            return f"Stack {stack_name} does not exist."
    elif "pop from stack" in command:
        stack_name = parts[-1]
        if stack_name in globals() and globals()[stack_name]:
            item = globals()[stack_name].pop()
            return f"Popped {item} from {stack_name}."
        else:
            return f"Stack {stack_name} does not exist or is empty."
    
    # Binary Trees
    elif "create a binary tree called" in command:
        tree_name = parts[-1]
        globals()[tree_name] = None
        return f"Binary tree {tree_name} created."
    elif "insert" in command and "into binary tree" in command:
        value = parts[1]
        tree_name = parts[-1]
        if tree_name in globals():
            globals()[tree_name] = insert(globals()[tree_name], value)
            return f"Inserted {value} into {tree_name}."
        else:
            return f"Binary tree {tree_name} does not exist."
    
    else:
        return "I don't understand that data structure command."

# Helper function for binary tree insertion
def insert(node, value):
    if node is None:
        return {'value': value, 'left': None, 'right': None}
    else:
        if value < node['value']:
            node['left'] = insert(node['left'], value)
        else:
            node['right'] = insert(node['right'], value)
    return node
