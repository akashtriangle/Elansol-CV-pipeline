import json
import asyncio
import websockets
from database import create_sqlite_db, insert_sqlite_db
import sqlite3

# web socket client, receives json from part2()
async def web_socket_client(event_json):
    uri = "ws://localhost:5000"
    async with websockets.connect(uri) as websocket:
        await websocket.send(event_json)


# web socket server, it receives from ws client and writes to sqlite db
async def web_socket_server():
    async def handler(websocket):
        async for event_data in websocket:
            data = json.loads(event_data) 
            insert_sqlite_db(data)        
            print(f"Data Stored: {data}")

    # this opens the port
    async with websockets.serve(handler, "localhost", 5000):
        await asyncio.Future() 

