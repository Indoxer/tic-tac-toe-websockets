from fastapi import WebSocket
import uuid

class Player:
    objects = []
    
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
        self.id = uuid.uuid4()
        self.room = None
        self.username = None
    
    async def send_message(self, action, payload):
        await self.websocket.send_json(dict(action=action, payload=payload))
    
    @property
    def reduced(self):
        return dict(
            username=self.username,
            id=str(self.id)
        )
    
    @property
    def personal(self):
        return dict(
            room=self.room.reduced,
            **self.reduced
        )
    
    def __eq__(self, obj: object) -> bool:
        if not isinstance(obj, Player):
            raise NotImplementedError
        
        return self.id == obj.id