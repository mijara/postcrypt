import json
import os


class InputStorage:
    def __init__(self, base_dir, save):
        self.input_file = os.path.join(base_dir, '.crypt-input.json')
        self.save = save
        self.saved_input = {} if not save else self._initialize()

    def set_input(self, key, value):
        self.saved_input[key] = value

        if self.save:
            self._store()

    def get_input(self, key):
        return self.saved_input[key]

    def has_input(self, key):
        return key in self.saved_input

    def _initialize(self):
        if os.path.exists(self.input_file):
            with open(self.input_file, 'r') as f:
                return json.load(f)
        else:
            return {}

    def _store(self):
        with open(self.input_file, 'w') as f:
            json.dump(self.saved_input, f)
