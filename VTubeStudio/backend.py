from vts import VTSController
from streamcontroller_plugin_tools import BackendBase
import rpyc

class Backend(BackendBase):
    def __init__(self):
        super().__init__()
        self.conn = rpyc.connect("localhost", 18812)

    def get_connected(self):
        return self.conn.root.get_connected()

    def connect_auth(self):
        return self.conn.root.connect_auth()

    def getHotkeys(self)->list[str]:
        return self.conn.root.get_hotkeys()

    def triggerHotkey(self, hotkey: str)->bool:
        return self.conn.root.trigger_hotkey(hotkey)

    def moveModel(self, x: float, y: float, rot: int, size: int, relative: bool, move_time: float)->bool:
        return self.conn.root.move_model(x, y, rot, size, relative, move_time)

    def getModelPosition(self):
        return self.conn.root.get_model_postion(self)

backend = Backend()

