import json
import os

DUNGEONS_STANDARD_PATH = "content/dungeons/standard"
DUNGEONS_SPECIAL_PATH = "content/dungeons/special"

ENCOUNTERS_STANDARD_PATH = "content/encounters/standard"
ENCOUNTERS_SPECIAL_PATH = "content/encounters/special"

ENEMIES_STANDARD_PATH = "content/enemies/standard"
ENEMIES_SPECIAL_PATH = "content/enemies/special"

STORY_PATH = "content/story"


def load_content_files(dir_path: str) -> dict:
    """
    Load all JSON files in the given directory and merge their contents into a single dictionary.
    """
    combined_content = {}

    # Walk through the directory and look for JSON files
    for root, _dirs, files in os.walk(dir_path):
        for file_name in files:
            if file_name.endswith(".json"):
                file_path = os.path.join(root, file_name)
                with open(file_path, "r") as file:
                    content_object = json.load(file)
                    if not isinstance(content_object, dict):
                        raise ValueError(
                            f"The file {file_path} does not contain a valid JSON object."
                        )
                    # Merge the content into the combined dictionary
                    combined_content.update(content_object)

    return combined_content


def load_enemy_content_files(dir_path) -> dict:
    combined_content = {"small_enemies": [], "medium_enemies": [], "large_enemies": []}
    # Walk through the directory and look for JSON files
    for root, dirs, files in os.walk(dir_path):
        for file_name in files:
            if file_name.endswith(".json"):
                file_path = os.path.join(root, file_name)
                with open(file_path, "r") as file:
                    content_object = json.load(file)
                    if not isinstance(content_object, dict):
                        raise ValueError(
                            f"The file {file_path} does not contain a valid JSON object."
                        )
                    # Merge the content into the combined dictionary
                    for key in combined_content:
                        if key in content_object:
                            combined_content[key].extend(content_object[key])

    return combined_content


DUNGEONS_STANDARD = load_content_files(DUNGEONS_STANDARD_PATH)
DUNGEONS_SPECIAL = load_content_files(DUNGEONS_SPECIAL_PATH)
ENCOUNTERS_STANDARD = load_content_files(ENCOUNTERS_STANDARD_PATH)
ENCOUNTERS_SPECIAL = load_content_files(ENCOUNTERS_SPECIAL_PATH)
ENEMIES_STANDARD = load_enemy_content_files(ENEMIES_STANDARD_PATH)
ENEMIES_SPECIAL = load_content_files(ENEMIES_SPECIAL_PATH)
ENCOUNTERS_SPECIAL = load_content_files(ENCOUNTERS_SPECIAL_PATH)
STORY = load_content_files(STORY_PATH)
