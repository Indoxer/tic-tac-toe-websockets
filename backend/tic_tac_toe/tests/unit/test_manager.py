import pytest

from unittest import mock

from tic_tac_toe.manager import ConnectionManager

import tic_tac_toe.player as pl

def test_init():
    actions = {"test":lambda player: None}
    manager = ConnectionManager(actions)
    
    assert manager._actions == actions

# payload is None
@pytest.mark.asyncio
async def test_process_1():
    action = "test"
    player = mock.Mock(spec=pl.Player)
    payload = None
    actions = {"test":lambda player: None}
    
    manager = ConnectionManager(actions)
    manager._process_action = mock.AsyncMock()
    
    await manager.process(action, player, payload)
    
    manager._process_action.assert_awaited_once_with(action, player, dict())
    
# Unknown action
@pytest.mark.asyncio
async def test_process_2():
    action = "test"
    player = mock.Mock(spec=pl.Player)
    payload = None
    actions = {}
    
    manager = ConnectionManager(actions)
    manager._process_action = mock.AsyncMock()
    
    with pytest.raises(ValueError) as e:
        await manager.process(action, player, payload)
        
    assert str(e.value) == f"Unknown Action: {action}"
 
    assert manager._process_action.called == False
    
# __process_action error
@pytest.mark.asyncio
async def test_process_3():
    action = "test"
    player = mock.Mock(spec=pl.Player)
    payload = {"test":"test"}

    actions = {"test":lambda player: None}
    
    manager = ConnectionManager(actions)
    manager._process_action = mock.AsyncMock()
    manager._process_action.side_effect = ValueError("test")
    
    with pytest.raises(ValueError) as e:
        await manager.process(action, player, payload)
        
    assert str(e.value) == "Unknown Server Error, check sended data!"
    manager._process_action.assert_awaited_once_with(action, player, payload)

# With action as one function
@pytest.mark.asyncio
async def test__process_1():
    func = mock.AsyncMock()
    payload = dict(test="test", test_2=None)
    action = "test"
    actions = {action:func}
    player = mock.Mock(spec=pl.Player)
    
    manager = ConnectionManager(actions)
    
    await manager._process_action(action, player, payload)
    
    func.assert_awaited_once_with(player=player, **payload)
    
# With action as one list of functions
@pytest.mark.asyncio
async def test__process_2():
    mocks_manager = mock.Mock()
    
    func_1 = mock.AsyncMock()
    func_2 = mock.AsyncMock()
    
    mocks_manager.attach_mock(func_1, "f_1")
    mocks_manager.attach_mock(func_2, "f_2")
    
    payload = dict(test="test", test_2=None)
    action = "test"
    actions = {action:[func_1, func_2]}
    player = mock.Mock(spec=pl.Player)
    
    manager = ConnectionManager(actions)
    
    await manager._process_action(action, player, payload)
    
    expected_calls = [mock.call.f_1(player=player, **payload), mock.call.f_2(player=player, **payload)]
    assert mocks_manager.mock_calls == expected_calls
    func_1.assert_awaited_once()
    func_2.assert_awaited_once()