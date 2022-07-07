import uuid
import pytest

from fastapi import WebSocket

from unittest import mock

import tic_tac_toe.player as pl

def test_objects():
    player_1 = pl.Player(mock.Mock(spec=WebSocket))
    player_2 = pl.Player(mock.Mock(spec=WebSocket))
    player_3 = pl.Player(mock.Mock(spec=WebSocket))
    pl.Player.objects = [player_1, player_2, player_3]
    
    import tic_tac_toe.player as pl2
    
    assert pl2.Player.objects == pl.Player.objects
    
def test_init():
    websocket = mock.Mock(spec=WebSocket)
    player = pl.Player(websocket)
    
    assert player.websocket == websocket
    assert isinstance(player.id, uuid.UUID)
    assert player.room == None
    assert player.username == None

@pytest.mark.asyncio
async def test_send_message():
    websocket = mock.Mock(spec=WebSocket)
    player = pl.Player(websocket)
    
    action = "test"
    payload = dict(name="test")
    
    await player.send_message(action, payload)
    
    websocket.send_json.assert_awaited_once_with(dict(action=action, payload=payload))
    
@pytest.mark.asyncio
async def test_reduced():
    websocket = mock.Mock(spec=WebSocket)
    player = pl.Player(websocket)
    player.username = "test"
    player.room = mock.Mock()
    
    assert player.reduced == dict(username=player.username, id=str(player.id))
    
@pytest.mark.asyncio
async def test_personal():
    websocket = mock.Mock(spec=WebSocket)
    player = pl.Player(websocket)
    player.username = "test"
    
    player.room = mock.Mock()
    player.room.reduced = "test"
    
    assert player.personal == dict(username=player.username, id=str(player.id), room="test")
    
def test_eq():
    websocket_1 = mock.Mock(spec=WebSocket)
    player_1 = pl.Player(websocket_1)
    
    websocket_2 = mock.Mock(spec=WebSocket)
    player_2 = pl.Player(websocket_2)
    
    assert not player_1 == player_2
    assert player_1 == player_1
    
    with pytest.raises(NotImplementedError):
        player_1 == "not working"
        
    