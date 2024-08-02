from .dictObj import dictObj
import yaml

class yamlConf(dictObj):

    def __init__(self, path = None):
        self.path = path
        self.load()

    def load(self):
        if self.path:
            with open(self.path, 'r') as stream:
                super().__load__(yaml.safe_load(stream))

    def save(self):
        out = self.__to_dict__().copy()
        with open(self.path, 'w') as stream:
            stream.write(yaml.safe_dump(out))
