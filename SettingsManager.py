import json
import os


class SettingsManager():
    def __init__(self, path: str = None):
        self.path = path if path else os.path.abspath(
            os.path.join(__file__, '..'))
        self.filename = 'settings.json'
        self.filepath = os.path.join(self.path, self.filename)
        self.settings = None
        self.load()

    def load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, encoding='utf-8') as f:
                self.settings = json.load(f)
        else:
            print("Settings file doesn't exits. Create one")
            self.create_default()

    def save(self):
        with open(os.path.join(self.path, self.filename), 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, indent=4)

    def create_default(self):
        self.settings = {
            'data': {
                'target_income': 3000.00,
            },
            'basic': {
                'data_path': os.path.join(self.path, 'data.json'),
                'autosave': True,
            },
            'style': {
                'order_color': '#c0fdff',
                'income_color': '#d0d1ff',
            }
        }
        self.save()
