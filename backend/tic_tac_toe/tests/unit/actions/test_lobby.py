from __future__ import annotations

import pytest

import tic_tac_toe.player as pl
import tic_tac_toe.room as ro

from tic_tac_toe.actions import lobby

from unittest import mock

@mock.patch("tic_tac_toe.room.Room")
@pytest.mark.asyncio
async def test_find_room_1(mocked_room):
    player = mock.AsyncMock(spec=pl.Player)
    player.reduced = dict()
    player.room = None
    
    username = "test"
    
    mocked_room.objects = []
    
    # Without spec=ro.Room because patch mocks this object.
    room = mock.AsyncMock()
    
    room.players = []
    room.reduced = dict()
    
    mocked_room.return_value = room
    
    await lobby.find_room(player, username)
    
    assert player.username == username
    
    assert len(mocked_room.objects) == 1
    assert mocked_room.objects[0] == room
    
    room.broadcast.assert_awaited_once_with("new_player", player.reduced)
    assert room.players == [player]
    player.send_message.assert_awaited_once_with("join_room", room.reduced)

@mock.patch("tic_tac_toe.room.Room")
@pytest.mark.asyncio
async def test_find_room_1(mocked_room):
    player = mock.AsyncMock(spec=pl.Player)
    player.reduced = dict()
    player.room = None
    
    username = "test"
    
    # Without spec=ro.Room because patch mocks this object.
    room = mock.AsyncMock()
    mocked_room.objects = [room]
    
    room.players = [mock.Mock()] * (lobby.MAX_PLAYERS_IN_ROOMS - 1)
    room.reduced = dict()
    
    await lobby.find_room(player, username)
    
    assert player.username == username
    
    assert len(mocked_room.objects) == 1
    assert mocked_room.called == False
    
    room.broadcast.assert_awaited_once_with("new_player", player.reduced)
    player.send_message.assert_awaited_once_with("join_room", room.reduced)

@mock.patch("tic_tac_toe.actions.base.error")
@pytest.mark.asyncio
async def test_find_room_3(mocked_error):
    player = mock.AsyncMock(spec=pl.Player)
    
    player.room = mock.Mock()
    
    username = "test"
    
    await lobby.find_room(player, username)
    
    mocked_error.assert_awaited_once_with(player, "Player has already room!")