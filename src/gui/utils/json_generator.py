import json

class JsonGenerator:

    def new_json(self, title: str):
        dictionary = {}
        json_object = json.dumps(dictionary, indent=4)
        json_file_path = str(title) + ".json"
        with open(json_file_path, "w") as outfile:
            outfile.write(json_object)
        return json_file_path

    def string_to_json(self, title: str, content: str):
        data = json.loads(content)
        json_title = str(title) + '.json'
        with open(json_title, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        return json_title

