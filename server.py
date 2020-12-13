import websockets
import asyncio
import aspects

from config import connConfig

CONFIG_PATH = "server_cfg/connection.json"

async def login(websocket, path):
    async for message in websocket:
        await websocket.send("Server response: {}".format(message))


config = connConfig()
config.load(CONFIG_PATH)

start_server = websockets.serve(login, config.URL, config.PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
