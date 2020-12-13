#!/usr/bin/python3

import asyncio
import websockets
import aspects

from config import connConfig

CONFIG_PATH = "client_cfg/connection.json"

config = connConfig()
config.load(CONFIG_PATH)

uri = "ws://{}:{}".format(config.URL, config.PORT)

async def hello():
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello world!")
        print(await websocket.recv())


asyncio.get_event_loop().run_until_complete(hello())
