import json

DUNGEONS_STANDARD_PATH = 'content/dungeons/standard'
DUNGEONS_SPECIAL_PATH = 'content/dungeons/special'

ENCOUNTERS_STANDARD_PATH = 'content/encounters/standard'
ENCOUNTERS_SPECIAL_PATH = 'content/encounters/special'

ENEMIES_STANDARD_PATH = 'content/enemies/standard'
ENEMIES_STANDARD_PATH = 'content/enemies/special'

STORY_PATH = 'content/story'


def load_content_file(path) -> dict:
    with open(path, 'r') as file:
        content_object = json.load(file)
    return content_object

