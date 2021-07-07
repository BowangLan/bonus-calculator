import json


class DataLoaderBase(object):
    def __init__(self, data_path, **kwargs):
        self.data_path = data_path

        # default arguments for open()
        kwargs['encoding'] = 'utf-8'
        self.kwargs = kwargs

    def load_data(self) -> list:
        pass


class JSONDataLoader(DataLoaderBase):

    def load_data(self):
        with open(self.data_path, **self.kwargs) as f:
            data = json.load(f)
        return data


class UserInputDataLoader(DataLoaderBase):

    def load_data(self):
        pass
