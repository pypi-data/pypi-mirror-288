import json
import os


class CachedModel:
    @staticmethod
    def get(lang):
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path) + "/"
        json_file = dir_path + f"data/model_{lang}.json"

        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data
