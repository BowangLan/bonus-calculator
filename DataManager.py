import json
import os


class DataManagerBase(object):
    def __init__(self, data_path: str = None, default_value=[], **kwargs):
        self.data_path = data_path
        self.data = default_value

        # default arguments for open()
        kwargs['encoding'] = 'utf-8'
        self.kwargs = kwargs

    def load_data(self) -> list:
        pass

    def save_data(self) -> None:
        pass


class JSONDataManager(DataManagerBase):

    def load_data(self):
        if os.path.exists(self.data_path):
            with open(self.data_path, **self.kwargs) as f:
                self.data = json.load(f)
            return self.data
        else:
            self.save_data()
            return self.data

    def save_data(self):
        with open(self.data_path, 'w', **self.kwargs) as f:
            json.dump(self.data, f, indent=4)


class SettingsManager():
    def __init__(self, path: str = None):
        self.path = path if path else os.path.abspath(
            os.path.join(__file__, '..'))
        self.filename = 'settings.json'
        self.filepath = os.path.join(self.path, self.filename)
        self.settings = None
        self.load_data()

    def load_data(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, encoding='utf-8') as f:
                self.settings = json.load(f)
        else:
            print("Settings file doesn't exits. Create one")
            self.create_default()

    def save_data(self):
        with open(os.path.join(self.path, self.filename), 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, indent=4)

    def create_default(self):
        self.settings = {
            'data': {
                'target_income': 3000.00,
                'bonus_rules': [],
            },
            'basic': {
                'cache_path': os.path.join(self.path, 'cache.json'),
                'autoopen_data_path': os.path.join(self.path, 'data.json'),
                'autosave': True,
            },
            'style': {
                'order_color': '#c0fdff',
                'income_color': '#d0d1ff',
            }
        }
        self.save_data()
