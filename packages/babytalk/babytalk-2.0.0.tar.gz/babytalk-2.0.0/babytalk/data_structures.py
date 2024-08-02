from collections import deque

def data_structures_execute(command):
    command = command.lower()
    words = command.split()

    try:
        # Lists
        if "make a list named" in command:
            list_name = words[-1]
            globals()[list_name] = []  # Create an empty list
            return f"Ok, I made a list named {list_name}."

        elif "add" in words and "to list" in words:
            item = words[1]  # The word after "add"
            list_name = words[-1]  # The word after "to list"
            globals()[list_name].append(item)  # Append to list
            return f"I added {item} to the list {list_name}."

        # Sets
        elif "make a set named" in command:
            set_name = words[-1]
            globals()[set_name] = set()  # Create an empty set
            return f"Ok, I made a set named {set_name}."

        elif "add" in words and "to set" in words:
            item = words[1]  # The word after "add"
            set_name = words[-1]  # The word after "to set"
            globals()[set_name].add(item)  # Add to set
            return f"I added {item} to the set {set_name}."

        # Queues (Waiting Lines)
        elif "make a waiting line named" in command:  
            queue_name = words[-1]
            globals()[queue_name] = deque()  # Create an empty queue
            return f"Ok, I made a waiting line named {queue_name}."

        elif "add" in words and "to waiting line" in command:
            item = words[1]  # The word after "add"
            queue_name = words[-1]  # The word after "to waiting line"
            globals()[queue_name].append(item)  # Append to queue
            return f"I added {item} to the back of the waiting line {queue_name}."

        elif "next in line from" in command:  
            queue_name = words[-1]
            item = globals()[queue_name].popleft()  # Remove from front of queue
            return f"{item} is next in line from {queue_name}."

        # Basic Binary Trees (Simplified) - Only insertion
        elif "make a tree named" in command:
            tree_name = words[-1]
            globals()[tree_name] = None  # Initialize empty tree
            return f"Ok, I made a tree named {tree_name}."

        elif "add" in words and "to tree" in command:
            value = int(words[1])  # Assuming integer values
            tree_name = words[-1]
            globals()[tree_name] = insert(globals()[tree_name], value)  # Insert into tree
            return f"I added {value} to the tree {tree_name}."

        else:
            return "I don't understand that."

    except (IndexError, ValueError, KeyError):  # Handle missing/invalid inputs
        return "Oops! Something's wrong with your command. Try again."

def insert(node, value):
    if node is None:
        return {'value': value, 'left': None, 'right': None}
    if value < node['value']:
        node['left'] = insert(node['left'], value)
    else:
        node['right'] = insert(node['right'], value)
    return node


