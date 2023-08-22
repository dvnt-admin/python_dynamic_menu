"""
Script Menu with Dynamic Options

This script presents a simple script menu with options that are dynamically
loaded from script files in a specified directory. The user can select an option
by entering the corresponding number. Each script file contains information
about the script's name and description in a specific format.

Example of a script file in the SCRIPT_DIR:
    # SCRIPT_NAME: Sample Script
    # SCRIPT_INFO: This is an example script description.
    import module_name
    # ... (rest of the script)

Usage:
    Place your script files in the '...' directory.
    Each script file should have lines '# SCRIPT_NAME:' and '# SCRIPT_INFO:'
    followed by the script's name and description. The actual script code can
    follow these lines.

"""

import os
import importlib.util

# Define the script directory
SCRIPT_DIR = "your path to the script directory goes here"

def load_scripts(script_dir):
    scripts = []
    for filename in os.listdir(script_dir):
        if filename.endswith('.py'):
            scripts.append(os.path.join(script_dir, filename))
    return scripts

def extract_info(script_path):
    script_name = ""
    script_info = ""
    with open(script_path, 'r') as script_file:
        for line in script_file:
            if line.startswith("# SCRIPT_NAME:"):
                script_name = line.split("[")[1].split("]")[0].strip()
            elif line.startswith("# SCRIPT_INFO:"):
                script_info = line.split("[")[1].split("]")[0].strip()
            elif line.strip() == "":
                break
    return script_name, script_info

def display_box(content):
    lines = content.strip().split('\n')
    max_length = max(len(line) for line in lines)
    box = f"\n\n┏{'━' * (max_length + 2)}┓\n"
    for line in lines:
        box += f"┃ {line.ljust(max_length)} ┃\n"
    box += f"┗{'━' * (max_length + 2)}┛\n\n"
    print(box)

def display_menu(script_list):
    menu = "Choose a script to run:\n"
    for idx, script_path in enumerate(script_list, start=1):
        script_name, script_info = extract_info(script_path)
        option = f"{idx}. {script_name} - {script_info}"
        menu += option + "\n"
    display_box(menu)

def main():
    scripts = load_scripts(SCRIPT_DIR)
    
    if not scripts:
        print("No scripts found in the directory.")
        return
    
    display_menu(scripts)
    choice = input("Enter the number of the script to run: ")

    try:
        choice_idx = int(choice) - 1
        if 0 <= choice_idx < len(scripts):
            chosen_script = scripts[choice_idx]
            print(f"Running {chosen_script}...\n")
            
            # Extract script name for module import
            script_name, _ = extract_info(chosen_script)
            script_module_name = os.path.splitext(os.path.basename(chosen_script))[0]
            
            # Import and run the chosen script
            try:
                module_spec = importlib.util.spec_from_file_location(script_module_name, chosen_script)
                module = importlib.util.module_from_spec(module_spec)
                module_spec.loader.exec_module(module)
            except Exception as e:
                print(f"An error occurred while running {chosen_script}: {e}")
                
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    main()
