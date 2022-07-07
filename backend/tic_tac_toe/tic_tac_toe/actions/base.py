from __future__ import annotations
import tic_tac_toe.player as pl

async def connect(player: pl.Player):
    await player.websocket.accept()
    pl.Player.objects.append(player)
    await player.send_message("connected", payload=player.reduced)
    
async def disconnect(player: pl.Player):
    pl.Player.objects.remove(player)
    
async def error(player: pl.Player, message: str):
    await player.send_message("__error__", dict(message=message))
