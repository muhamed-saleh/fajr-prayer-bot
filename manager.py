import json
import sys

CONFIG_FILE = 'config.json'

def load_groups():
    """Loads groups from the config file, creating it if it doesn't exist."""
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f).get('groups', [])
    except (FileNotFoundError, json.JSONDecodeError):
        # If file is missing or empty/invalid, start with an empty list
        return []

def save_groups(groups):
    """Saves the list of groups back to the config file."""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump({'groups': groups}, f, indent=2, ensure_ascii=False)

def list_groups():
    """Prints the current list of groups."""
    groups = load_groups()
    if not groups:
        print("No groups found in the configuration.")
        return
    print("Current groups in config.json:")
    for i, group in enumerate(groups, 1):
        print(f"  {i}. Name: '{group['name']}', ID: {group['id']}")

def add_group(name, group_id):
    """Adds a new group to the configuration."""
    groups = load_groups()
    # Check if group name or ID already exists
    if any(g['name'] == name for g in groups):
        print(f"Error: A group with the name '{name}' already exists.")
        return
    if any(g['id'] == group_id for g in groups):
        print(f"Error: A group with the ID '{group_id}' already exists.")
        return
    
    groups.append({'name': name, 'id': int(group_id)})
    save_groups(groups)
    print(f"Successfully added group: '{name}'")
    list_groups()

def remove_group(name):
    """Removes a group from the configuration by its name."""
    groups = load_groups()
    original_count = len(groups)
    groups_to_keep = [g for g in groups if g['name'] != name]
    
    if len(groups_to_keep) == original_count:
        print(f"Error: No group found with the name '{name}'.")
        return
        
    save_groups(groups_to_keep)
    print(f"Successfully removed group: '{name}'")
    list_groups()

def print_help():
    """Prints the help message."""
    print("\n--- Group Manager for Telegram Bot ---")
    print("Usage: python manager.py [command] [arguments]")
    print("\nCommands:")
    print("  list                - Shows all current groups.")
    print("  add <'Name'> <ID>   - Adds a new group. (Note: Use quotes for names with spaces)")
    print("  remove <'Name'>     - Removes a group by its name.")
    print("\nExamples:")
    print("  python manager.py list")
    print("  python manager.py add 'Family Group' -100123456")
    print("  python manager.py remove 'Family Group'")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
    else:
        command = sys.argv[1]
        if command == 'list':
            list_groups()
        elif command == 'add' and len(sys.argv) == 4:
            add_group(name=sys.argv[2], group_id=sys.argv[3])
        elif command == 'remove' and len(sys.argv) == 3:
            remove_group(name=sys.argv[2])
        else:
            print("Error: Invalid command or wrong number of arguments.")
            print_help()