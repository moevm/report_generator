import json
JSON_FILE = 'settings.json'


class json_api:

    def __init__(self):
        self.read_json_file()
        self.change_content()
        self.write_json_file()
        pass

    def read_json_file(self):
        with open(JSON_FILE, 'r') as file:
            self.json_data = json.load(file)

    def write_json_file(self):
        with open(JSON_FILE, 'w') as file:
            file.write(json.dumps(self.json_data))

    def change_content(self):
        print(self.json_data)


if __name__ == '__main__':
    app = json_api()

