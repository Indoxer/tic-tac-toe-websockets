from __future__ import annotations
from fastapi import WebSocket

import pytest

import tic_tac_toe.player as pl

from tic_tac_toe.actions import base

from unittest import mock

@mock.patch.object(pl.Player, 'objects', new_callable=mock.PropertyMock)
@pytest.mark.asyncio
async def test_connect(mocked_objects):
    player = mock.Mock(spec=pl.Player)
    
    player.websocket = mock.AsyncMock(spec=WebSocket)
    player.reduced = dict()
    
    mocked_objects.return_value = []
    
    await base.connect(player)
    
    player.websocket.accept.assert_awaited_once()

    assert mocked_objects.return_value == [player]
    player.send_message.assert_awaited_once_with("connected", payload=player.reduced)
    
@mock.patch.object(pl.Player, 'objects', new_callable=mock.PropertyMock)
@pytest.mark.asyncio
async def test_disconnect(mocked_objects):
    player = mock.Mock(spec=pl.Player)
    
    mocked_objects.return_value = [player]
    
    await base.disconnect(player)

    assert mocked_objects.return_value == []

@pytest.mark.asyncio
async def test_error():
    player = mock.AsyncMock(spec=pl.Player)
    
    message = "test"
    
    await base.error(player, message)

    player.send_message.assert_awaited_once_with("__error__", dict(message=message))
    
    
    
