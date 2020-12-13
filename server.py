import websockets
import asyncio
import aspects
import json
import utils

import logger

from config import connConfig

CONFIG_PATH = "server_cfg/connection.json"

user_db = "database/users.json"

@logger.log_exception
def search_user(user):
    with open(user_db) as fp:
        users = json.load(fp)
        return user in users.keys()

@logger.log_exception
def login_user(user, password):
    with open(user_db) as fp:
        users = json.load(fp)
        try:
            return users[user] == password
        except Exception as e:
            raise

@logger.log_exception
def append_user(user, password):
    with open(user_db, 'r') as fp:
        users = json.load(fp)
        users.update({user: password})
    utils.dump_json(user_db, users)

@logger.log_exception
async def handler(websocket, path):
    async for message in websocket:
        if json.loads(message).get('request') == "register":
            print (json.loads(message))
            await websocket.send("ok")
            creds = await websocket.recv()
            print(creds)
            if not utils.validate_user(creds):
                await websocket.send("error")
            creds = json.loads(creds)
            if search_user(creds['usr']):
                await websocket.send("error")
            else:
                append_user(creds['usr'], creds['pwd'])
                await websocket.send("success")

        elif json.loads(message).get('request') == 'login':
            print(json.loads(message))
            await websocket.send("ok")
            creds = await websocket.recv()
            print(creds)
            if not utils.validate_user(creds):
                await websocket.send("error")
            creds = json.loads(creds)
            if login_user(creds['usr'], creds['pwd']):
                await websocket.send("success")
            else:
                await websocket.send("error")

        await websocket.send("Server response: Login attempt from {}".format(
        websocket.local_address))


config = connConfig()
config.load(CONFIG_PATH)

start_server = websockets.serve(handler, config.URL, config.PORT)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
