import websockets
import asyncio
import json
import utils
import aspects

CONFIG_PATH = "server_cfg/server.json"

class Config():
    def __init__(self):
        self.URL = ""
        self.PORT = 9999
        self.columns = ['URL', 'PORT']

    def validateConfig(self, config):
        if set(config.keys()) != set(self.columns):
            # map(lambda x,y: print("{} != {}".format(x,y)), set(config.keys()), set(self.columns))
            return False

        return True

    def load(self, path):
        data = utils.load_json(path)['config']
        if self.validateConfig(data):
            self.URL = data['URL']
            self.PORT = int(data['PORT'])
        else:
            print("Could not load json. Check to contain the following fields: \
            {}".format(self.columns))

async def main(websocket, path):
    async for message in websocket:
        await websocket.send(message)

config = Config()
config.load(CONFIG_PATH)

start_server = websockets.serve(main, config.URL, config.PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
