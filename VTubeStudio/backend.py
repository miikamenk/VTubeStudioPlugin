import asyncio
import concurrent.futures.thread    # ← the pre‐load
from vts import VTSController
from streamcontroller_plugin_tools import BackendBase

class Backend(BackendBase):
    def __init__(self):
        super().__init__()
        # ① new loop, ② set it as current
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        self.vtsc = VTSController()

    def connect_auth(self):
        return self.loop.run_until_complete(self.vtsc.connect_auth())

    def getHotkeys(self) -> list[str]:
        return self.loop.run_until_complete(self.vtsc.getHotkeys())

    def triggerHotkey(self, hotkey: str) -> bool:
        return self.loop.run_until_complete(self.vtsc.triggerHotkey(hotkey))

    def moveModel(self, *args, **kwargs) -> bool:
        return self.loop.run_until_complete(self.vtsc.moveModel(*args, **kwargs))
