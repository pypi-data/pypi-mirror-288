from collections import deque

def data_structures_execute(command):
    command = command.lower()
    words = command.split()

    try:
        # Lists
        if "make a list named" in command:
            list_name = words[-1]
            globals()[list_name] = [] 
            return f"Ok, I made a list named {list_name}."

        elif "add" in words and "to list" in words:
            item = words[1] 
            list_name = words[-1] 

            # Check if the list exists
            if list_name not in globals():
                return f"Oops! I couldn't find a list named {list_name}."

            globals()[list_name].append(item)  
            return f"I added {item} to the list {list_name}."

        # Sets
        elif "make a set named" in command:
            set_name = words[-1]
            globals()[set_name] = set() 
            return f"Ok, I made a set named {set_name}."

        elif "add" in words and "to set" in words:
            item = words[1]  
            set_name = words[-1] 

            # Check if the set exists
            if set_name not in globals():
                return f"Oops! I couldn't find a set named {set_name}."

            globals()[set_name].add(item) 
            return f"I added {item} to the set {set_name}."

        # Queues (Waiting Lines)
        elif "make a waiting line named" in command:  
            queue_name = words[-1]
            globals()[queue_name] = deque() 
            return f"Ok, I made a waiting line named {queue_name}."

        elif "add" in words and "to waiting line" in command:
            item = words[1] 
            queue_name = words[-1]

            # Check if the queue exists
            if queue_name not in globals():
                return f"Oops! I couldn't find a waiting line named {queue_name}."

            globals()[queue_name].append(item)  
            return f"I added {item} to the back of the waiting line {queue_name}."

        elif "next in line from" in command:  
            queue_name = words[-1]

            # Check if the queue exists and is not empty
            if queue_name not in globals():
                return f"Oops! I couldn't find a waiting line named {queue_name}."
            if not globals()[queue_name]:
                return f"The waiting line {queue_name} is empty!"

            item = globals()[queue_name].popleft() 
            return f"{item} is next in line from {queue_name}."

        # Basic Binary Trees (Simplified) - Only insertion
        elif "make a tree named" in command:
            tree_name = words[-1]
            globals()[tree_name] = None 
            return f"Ok, I made a tree named {tree_name}."

        elif "add" in words and "to tree" in command:
            value = int(words[1]) 
            tree_name = words[-1]

            # Check if the tree exists
            if tree_name not in globals():
                return f"Oops! I couldn't find a tree named {tree_name}."

            globals()[tree_name] = insert(globals()[tree_name], value) 
            return f"I added {value} to the tree {tree_name}."

        else:
            return "I don't understand that."

    except (IndexError, ValueError, KeyError) as e:
        return f"Oops! Something's wrong with your command: {e}. Try again."

def insert(node, value):
    if node is None:
        return {'value': value, 'left': None, 'right': None}
    if value < node['value']:
        node['left'] = insert(node['left'], value)
    else:
        node['right'] = insert(node['right'], value)
    return node
