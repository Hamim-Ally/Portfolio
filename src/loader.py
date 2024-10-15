import os
import yaml

# Merge two dictionaries, with dict2 overwriting dict1.
def merge_dicts(dict1, dict2):
    result = dict1.copy() if dict1 else {}
    if dict2:
        result.update(dict2)
    print('   Data is merging...')
    return result

# ====================================
# Loader Functions
# ====================================

# Load a YAML file from the given path.
def load_yaml(file_path):
    try:
        with open(file_path, 'r') as file:
            print(f'{file_path} loaded...')
            return yaml.safe_load(file) or {}  # Return an empty dict if None
    except Exception as e:
        print(f"Error loading YAML file {file_path}: {e}")
        return {}  # Return empty dict in case of an error

# Load a widget file from the given path.
def load_widget(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            print(f'{file_path} loaded...')
            return file.read()  # Read widget content as string
    except Exception as e:
        print(f"Error loading widget file {file_path}: {e}")
        return ''  # Return empty string in case of an error

# List all YAML files from the given directory.
def load_pages(directory='src/pages'):
    try:
        pages = [f for f in os.listdir(directory) if f.endswith('.yml')]
        for page in pages:
            pass# print(f"{os.path.splitext(page)[0].capitalize()} page loaded...")
        return pages
    except FileNotFoundError:
        print(f"Directory '{directory}' not found.")
        return []

# ====================================
# Initialization Functions
# ====================================

# Load and merge all YAML files from a given directory.
def init_DataPack(directory):
    merged_data = {}
    try:
        for file_name in os.listdir(directory):
            if file_name.endswith('.yml'):
                file_path = os.path.join(directory, file_name)
                data = load_yaml(file_path)
                merged_data = merge_dicts(merged_data, data)  # Merge with the accumulated data
        print('Data Pack initialized.')
    except FileNotFoundError:
        print(f"Directory '{directory}' not found.")
    return merged_data

# Load and initialize widgets from a directory.
def init_widgets(directory):
    widgets = {}
    try:
        for file_name in os.listdir(directory):
            if file_name.endswith('.html'):
                widget_name = os.path.splitext(file_name)[0]
                widgets[widget_name] = load_widget(os.path.join(directory, file_name))
        print('Widgets initialized.')
    except FileNotFoundError:
        print(f"Directory '{directory}' not found.")
    return widgets
