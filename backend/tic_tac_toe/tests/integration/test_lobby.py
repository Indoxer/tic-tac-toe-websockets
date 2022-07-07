import pytest

import uuid
from fastapi.testclient import TestClient

from tic_tac_toe.app import app

client = TestClient(app)

def test_connect():
    with client.websocket_connect("/ws") as websocket:
        data = websocket.receive_json()
        
    assert data["action"] == "connected"
    assert isinstance(data["payload"], dict)
    uuid.UUID(data["payload"]["id"])
    
@pytest.mark.asyncio
async def test_connect_2():
    with client.websocket_connect("/ws") as websocket:
        websocket.receive_json()
        data = dict(
            action="find_room",
            payload=dict(
                username="test"
            )
        )
        websocket.send_json(data, mode="text")
        data = websocket.receive_json()
        
    assert data["action"] == "join_room"
    assert len(data["payload"]["players"]) == 1