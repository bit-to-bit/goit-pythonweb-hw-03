"""Storage module"""

import json
from pathlib import Path


class Storage:
    """Storage class"""

    DEFAULT_STORAGE_PATH = "./storage"

    def __init__(self):
        try:
            path = Path(self.DEFAULT_STORAGE_PATH)
            path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise e
        self.storage_path = path

    def save_data(self, dictionary_object: dict, filename: str = "data.json"):
        """Serialize object to storage"""

        with open(self.storage_path.joinpath(filename), "w", encoding="utf-8") as f:
            json.dump(dictionary_object, f)

    def load_data(self, filename: str = "data.json"):
        """Deserialize object from storage"""

        try:
            with open(self.storage_path.joinpath(filename), "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return None
