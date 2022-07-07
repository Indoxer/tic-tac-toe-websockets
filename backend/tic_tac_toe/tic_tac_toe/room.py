from typing import Dict
import uuid

class Room:
    objects = []
    
    def __init__(self):
        self.id = uuid.uuid4()
        self.players = []
        
    async def broadcast(self, action: str, payload: Dict):
        for player in self.players:
            await player.send_message(action, payload)
    
    @property
    def reduced(self):
        reduced_players = list(map(lambda player: player.reduced, self.players))
        return dict(
            players=reduced_players,
            id=str(self.id),
        )