from __future__ import annotations
import tic_tac_toe.player as pl
import tic_tac_toe.room as ro
from tic_tac_toe.actions import base

MAX_PLAYERS_IN_ROOMS = 2

async def find_room(player: pl.Player, username: str):
    if not player.room is None:
        await base.error(player, "Player has already room!")
        return None
    
    player.username = username
    
    rooms = list(filter(lambda room: len(room.players) < MAX_PLAYERS_IN_ROOMS, ro.Room.objects))
    
    if not rooms:
        room = ro.Room()
        ro.Room.objects.append(room)
    else:
        room = rooms[0]
    
    await room.broadcast("new_player", player.reduced)
    room.players.append(player)
    player.room = room
    await player.send_message("join_room", room.reduced)
        