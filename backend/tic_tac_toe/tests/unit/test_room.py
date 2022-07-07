import pytest

from unittest import mock
import uuid

import tic_tac_toe.room as ro
import tic_tac_toe.player as pl

def test_objects():
    room_1 = ro.Room()
    room_2 = ro.Room()
    
    ro.Room.objects = [room_1, room_2]
    
    import tic_tac_toe.room as ro2
    
    assert ro.Room.objects == ro2.Room.objects

def test_init():
    room = ro.Room()
    
    assert isinstance(room.id, uuid.UUID)
    assert room.players == []

@pytest.mark.asyncio
async def test_broadcast():
    room = ro.Room()
    
    action = "test"
    payload = dict()
    
    player_1 = mock.AsyncMock(spec=pl.Player)
    player_2 = mock.AsyncMock(spec=pl.Player)
    
    room.players = [player_1, player_2]
    
    await room.broadcast(action, payload)
    
    player_1.send_message.assert_awaited_once_with(action, payload)
    player_2.send_message.assert_awaited_once_with(action, payload)
    
def test_reduced():
    room = ro.Room()
    
    player = mock.AsyncMock(spec=pl.Player)
    player.reduced = "test"
    
    room.players = [player]
    
    assert room.reduced == dict(players=["test"], id=str(room.id))
    
    