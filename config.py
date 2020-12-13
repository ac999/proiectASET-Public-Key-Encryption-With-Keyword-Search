import utils

class Config():
    def __init__(self):
        self.columns = list()

    def validateConfig(self, config):
        if set(config.keys()) != set(self.columns):
            return False

        return True

class connConfig(Config):
    def __init__(self):
        self.URL = ""
        self.PORT = 9999
        self.columns = ['URL', 'PORT']

    def load(self, path):
        data = utils.load_json(path)['config']
        if self.validateConfig(data):
            self.URL = data['URL']
            self.PORT = int(data['PORT'])
        else:
            raise Exception("Could not load json. Check the following fields: \
            {}".format(self.columns))
