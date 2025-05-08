from streamcontroller_plugin_tools import BackendBase
from .vts import VTSController
import asyncio

class Backend(BackendBase):
    def __init__(self):
        super().__init__()
        
        self.vtsc = VTSController()
        self.loop = asyncio.get_event_loop()

    def connect_auth(self):
        return self.loop.run_until_complete(self.vtsc.connect_auth())
        
    def getHotkeys(self)->list[str]:
        return self.loop.run_until_complete(self.vtsc.getHotkeys())

    def triggerHotkey(self, hotkey: str)->bool:
        return self.loop.run_until_complete(self.vtsc.triggerHotkey(hotkey))

    def moveModel(self, x: float, y: float, rot: float, size: float, relative: bool, move_time: float)->bool:
        return self.loop.run_until_complete(
            self.vtsc.moveModel(x, y, rot, size, relative, move_time)
        )


backend = Backend()
