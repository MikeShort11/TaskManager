import json

class JsonGenerator:

    def new_json(self, title: str):
        dictionary = {}
        json_object = json.dumps(dictionary, indent=4)
        json_file_path = str(title) + ".json"
        with open(json_file_path, "w") as outfile:
            outfile.write(json_object)
        return json_file_path
