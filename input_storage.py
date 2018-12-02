import json
import os


class InputStorage:
    def __init__(self, base_dir):
        self.input_file = os.path.join(base_dir, '.crypt-input.json')

    def initialize(self):
        if os.path.exists(self.input_file):
            with open(self.input_file, 'r') as f:
                return json.load(f)
        else:
            return {}

    def store(self, saved_input):
        with open(self.input_file, 'w') as f:
            json.dump(saved_input, f)
