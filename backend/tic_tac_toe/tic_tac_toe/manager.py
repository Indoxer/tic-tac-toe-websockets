from __future__ import annotations

from typing import Dict, Callable

import tic_tac_toe.player as pl

class ConnectionManager:
    def __init__(self, actions_dict: Dict[str, Callable]):
        self._actions = actions_dict
    
    async def _process_action(self, action: str, player: pl.Player, payload: Dict):
        if isinstance(self._actions[action], list):
            for func in self._actions[action]:
                await func(player=player, **payload)
        else:
            func = self._actions[action]
            await func(player=player, **payload)
    
    async def process(self, action: str, player: pl.Player, payload: Dict = None):
        if payload is None:
            payload = dict()
        
        if action in self._actions:
            try:
                await self._process_action(action, player, payload)
            except Exception as e:
                print(e)
                raise ValueError(f"Unknown Server Error, check sended data!")
        else:
            raise ValueError(f"Unknown Action: {action}")