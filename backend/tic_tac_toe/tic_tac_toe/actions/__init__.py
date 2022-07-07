import tic_tac_toe.actions.base as base
import tic_tac_toe.actions.lobby as lobby

actions_dict = {
    "__connect__": base.connect,
    "__disconnect__": base.disconnect,
    "__error__": base.error,
    "find_room": lobby.find_room,
}