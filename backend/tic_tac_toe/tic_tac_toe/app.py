from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from tic_tac_toe.manager import ConnectionManager

app = FastAPI()

from tic_tac_toe.actions import actions_dict

manager = ConnectionManager(actions_dict)

import tic_tac_toe.player as pl

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    player = pl.Player(websocket)
    await manager.process("__connect__", player)
    try:
        while True:
            message = await websocket.receive_json()
            
            action = message.get("action", None)
            
            if action is None:
                await manager.process("__error__", player, dict(message="Action key is required!"))
            try:
                await manager.process(action, player, message.get("payload", dict()))
            except ValueError as e:
                await manager.process("__error__", player, dict(message=e.message))
            
    except WebSocketDisconnect:
        await manager.process("__disconnect__", player, dict())
    except Exception as e:
        await manager.process("__error__", player, dict(message="Unknown Error!"))
        await manager.process("__disconnect__", player, dict())