def data_structures_execute(command):
    try:
        parts = command.split()
        # Lists and Matrices
        if "create a list called" in command:
            list_name = parts[-1]
            exec(f"global {list_name}; {list_name} = []")
            return f"List {list_name} created."
        elif "add" in command and "to list" in command:
            item = parts[1]
            list_name = parts[4]
            exec(f"{list_name}.append({item})")
            return f"Added {item} to {list_name}."
        elif "create a matrix called" in command:
            matrix_name = parts[-1]
            exec(f"global {matrix_name}; {matrix_name} = []")
            return f"Matrix {matrix_name} created."
        elif "add row" in command and "to matrix" in command:
            row = eval(parts[2])
            matrix_name = parts[-1]
            exec(f"{matrix_name}.append({row})")
            return f"Added row {row} to {matrix_name}."
        
        # Sets
        elif "create a set called" in command:
            set_name = parts[-1]
            exec(f"global {set_name}; {set_name} = set()")
            return f"Set {set_name} created."
        elif "add" in command and "to set" in command:
            item = parts[1]
            set_name = parts[4]
            exec(f"{set_name}.add({item})")
            return f"Added {item} to {set_name}."
        
        # Queues
        elif "create a queue called" in command:
            queue_name = parts[-1]
            exec(f"global {queue_name}; {queue_name} = deque()")
            return f"Queue {queue_name} created."
        elif "enqueue" in command and "to queue" in command:
            item = parts[1]
            queue_name = parts[4]
            exec(f"{queue_name}.append({item})")
            return f"Enqueued {item} to {queue_name}."
        elif "dequeue from queue" in command:
            queue_name = parts[-1]
            exec(f"{queue_name}.popleft()")
            return f"Dequeued from {queue_name}."
        
        # Stacks
        elif "create a stack called" in command:
            stack_name = parts[-1]
            exec(f"global {stack_name}; {stack_name} = []")
            return f"Stack {stack_name} created."
        elif "push" in command and "to stack" in command:
            item = parts[1]
            stack_name = parts[4]
            exec(f"{stack_name}.append({item})")
            return f"Pushed {item} to {stack_name}."
        elif "pop from stack" in command:
            stack_name = parts[-1]
            exec(f"{stack_name}.pop()")
            return f"Popped from {stack_name}."
        
        # Binary Trees
        elif "create a binary tree called" in command:
            tree_name = parts[-1]
            exec(f"global {tree_name}; {tree_name} = None")
            return f"Binary tree {tree_name} created."
        elif "insert" in command and "into binary tree" in command:
            value = parts[1]
            tree_name = parts[-1]
            exec(f"{tree_name} = insert({tree_name}, {value})")
            return f"Inserted {value} into {tree_name}."
        
        else:
            return "I don't understand that data structure command."
    except Exception as e:
        return f"Error during execution: {e}"

def insert(node, value):
    if node is None:
        return {'value': value, 'left': None, 'right': None}
    else:
        if value < node['value']:
            node['left'] = insert(node['left'], value)
        else:
            node['right'] = insert(node['right'], value)
    return node
