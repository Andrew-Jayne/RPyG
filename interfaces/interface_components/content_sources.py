from abc import ABC, abstractmethod
from typing import Final, override

from RPyG.constructs import ContentDataDict


class ContentSource(ABC):
    @staticmethod
    @abstractmethod
    def get_content() -> dict[str, ContentDataDict]:
        pass


class ContentFileLoaderSource(ContentSource):
    CONTENT_PATH: Final[str] = "game_content"

    @override
    @staticmethod
    def get_content() -> dict[str, ContentDataDict]:
        """
        Load all JSON or TOML files in the given directory and merge their contents into a single dictionary.
        """
        import json
        import os
        import tomllib

        dir_path = ContentFileLoaderSource.CONTENT_PATH
        combined_content: dict[str, ContentDataDict] = {}

        # Walk through the directory and look for JSON files
        for root, _dirs, files in os.walk(dir_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                file_extension = os.path.splitext(file_path)[1]
                content_object: dict[str, ContentDataDict] = {}
                match file_extension:
                    case ".json":
                        with open(file_path, "r") as json_file:
                            content_object = json.load(json_file)
                    case ".toml":
                        with open(file_path, "rb") as toml_file:
                            content_object = tomllib.load(toml_file)
                    case _:
                        pass

                new_object = set(content_object.keys())
                all_content = set(combined_content.keys())
                conflicts = new_object.intersection(all_content)
                if conflicts == set():
                    combined_content.update(content_object)
                else:
                    raise ValueError(
                        f"Duplicate Key Declaration found while processing {file_path} conflicting keys {conflicts}"
                    )

        return combined_content
