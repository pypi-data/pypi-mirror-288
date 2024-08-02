import json
from pathlib import Path
from typing import Any, Dict

from nanoid import generate


def load_json_data(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r') as file:
        return json.load(file)


def save_json_data(file_path: str, data: Dict[str, Any]) -> None:
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def create_nano_id() -> str:
    disallowed = ['-', '_']
    nano_id = generate()
    while any([item in nano_id for item in disallowed]):
        nano_id = generate()
    return nano_id


def replace_uuids_with_nanoids(json_file_path: str, directory_path: str) -> None:
    data = load_json_data(json_file_path)
    for entry in data:
        old_id = entry['id']
        new_id = create_nano_id()
        entry['id'] = new_id

        # Rename the folder
        old_folder = Path(directory_path) / old_id
        new_folder = Path(directory_path) / new_id

        if old_folder.exists():
            old_folder.rename(new_folder)

    save_json_data(json_file_path, data)

# Usage
json_file_path = '/Users/asimshrestha/Documents/GitHub/bananalyzer/static/examples.json'  # Path to your JSON file
directory_path = '/Users/asimshrestha/Documents/GitHub/bananalyzer/static'  # Path to the directories
replace_uuids_with_nanoids(json_file_path, directory_path)
