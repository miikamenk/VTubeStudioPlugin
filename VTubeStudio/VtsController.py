import threading
import asyncio
import rpyc
from .vts import VTSController


class VTSControlService(rpyc.Service):
    def __init__(self):
        self.vtsc = VTSController()  # Use SyncVTSController to handle communication with VTube Studio

    def on_connect(self, conn):
        print(f"New connection: {conn}")

    def on_disconnect(self, conn):
        print(f"Connection closed: {conn}")

    def get_service_name():
        # Return the name of the service for logging purposes
        return "VTSControlService"

    def exposed_get_connected(self):
        return self.vtsc.get_connected

    def exposed_connect_auth(self):
        return self._run_async(self.vtsc.connect_auth)

    def exposed_get_hotkeys(self):
        return self._run_async(self.vtsc.getHotkeys)

    def exposed_trigger_hotkey(self, hotkey):
        return self._run_async(self.vtsc.triggerHotkey, hotkey)

    def exposed_move_model(self, x, y, rotation, size, relative, move_time):
        return self._run_async(self.vtsc.moveModel, x, y, rotation, size, relative, move_time)

    def _run_async(self, func, *args):
        """Helper to run async functions in a sync context."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(func(*args))  # Run async function synchronously

# Start the rpyc service
if __name__ == "__main__":
    from rpyc import ThreadingServer

    print("main entry hit")

    # Start the rpyc server to listen on port 18812
    server = ThreadingServer(VTSControlService, port=18812)
    print("Starting VTS control server on port 18812...")
    server.start()

