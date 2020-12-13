#!/usr/bin/python3

import asyncio
import websockets
import aspects

from os import system, name

from timeout_decorator import timeout

from time import sleep

import getpass

import utils
import logger

from config import connConfig

CONFIG_PATH = "client_cfg/connection.json"

LOGINTIMEOUT = 300
REGISTERTIMEOUT = 500
SIGNALS = True

config = connConfig()
config.load(CONFIG_PATH)

uri = "ws://{}:{}".format(config.URL, config.PORT)

def clear():
    # for windows
    if name == 'nt':
        system('cls')
    else:
        system('clear')

@logger.log_exception
def menu():
    error = False
    while True:
        x = -1
        if error:
            sleep(2)
        # clear()
        print("Welcome!\n")

        print("1. Login")
        print("2. Register")
        print("0. Exit")
        try:
            x = int(input("\nChoose: "))
        except Exception as e:
            print("Chosen action is not possible.")
            error = True

        if x == 0:
            print("Goodbye!")
            exit()

        if x == 1:
            try:
                resp = asyncio.get_event_loop().run_until_complete(login())
                error = False
            except Exception as e:
                print("Couldn't perform login.")
                error = True

        if x == 2:
            try:
                asyncio.get_event_loop().run_until_complete(register())
                error = False
            except Exception as e:
                print("Couldn't perform registration.")
                error = True


@logger.log_exception
@timeout(REGISTERTIMEOUT, use_signals = SIGNALS)
async def register():
    username = input("Username:")
    password = getpass.getpass("Password:")
    hibp = utils.hibp_password(password)
    if hibp[1]:
        if not hibp[0]:
            print("\nCould not verify if the password is compromised.\n")
    else:
        print("\nPassword is compromised. Must use another password.\n")
        raise Exception("Compromised password at registration phase.")
    rpassword = getpass.getpass("Repeat password:")
    if password != rpassword:
        print("\nPasswords are not the same.\n")
        raise Exception("Passwords differ at registration phase.")
    password = utils.hash(password)
    creds = utils.create_json(usr = username, pwd = password)
    if utils.validate_user(creds):
        async with websockets.connect(uri) as websocket:
            await websocket.send(utils.create_json(request = "register"))
            resp = await websocket.recv()
            if resp == "ok":
                await websocket.send(creds)
                resp = await websocket.recv()
                if resp == "success":
                    print("registration successful")
                else:
                    raise Exception('\nServer could not register the user.')
            else:
                raise Exception('\nServer could not register the user.')

@logger.log_exception
@timeout(LOGINTIMEOUT, use_signals = SIGNALS)
async def login():
    username = input("Username:")
    password = getpass.getpass("Password:")
    password = utils.hash(password)
    creds = utils.create_json(usr = username, pwd = password)
    if utils.validate_user(creds):
        async with websockets.connect(uri) as websocket:
            await websocket.send(utils.create_json(request = "login"))
            resp = await websocket.recv()
            if resp == "ok":
                await websocket.send(creds)
                resp = await websocket.recv()
                if resp == "success":
                    print("login successful")
                else:
                    raise Exception('\nUser could not log in.')
            else:
                raise Exception('\nUser could not log in.')

# menu()
asyncio.get_event_loop().run_until_complete(menu())
