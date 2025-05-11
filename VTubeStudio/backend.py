from vts import VTSController
from streamcontroller_plugin_tools import BackendBase
import rpyc
import asyncio
import time

import threading
from rpyc.utils.server import ThreadedServer
from VtsController import VTSControlService 



class Backend(BackendBase):
    def __init__(self):
        super().__init__()
        self.loop = asyncio.new_event_loop()
        self.loop_thread = threading.Thread(target=self.loop.run_forever, daemon=True)
        self.loop_thread.start()

        self.ensure_event_loop()

        self.server_thread = threading.Thread(target=self.start_inner_server, daemon=True)
        self.server_thread.start()

        # Ensure server is up before trying to connect
        self._wait_for_server()

        # After the server is confirmed to be running, initialize connection
        self.conn = rpyc.connect("localhost", 18812)

    
    def ensure_event_loop(self):
        if not asyncio.get_event_loop().is_running():
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)

    def _wait_for_server(self, timeout=5):
        """Wait for the server to be up before attempting to connect."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                # Try a simple ping to see if the server is ready
                rpyc.connect("localhost", 18812)
                print("Server is up and ready to accept connections.")
                return
            except rpyc.ConnectionError:
                time.sleep(0.1)  # Wait before retrying
        raise TimeoutError(f"Failed to connect to the server within {timeout} seconds.")

    def reconnect_if_needed(self):
        try:
            if self.conn is None or self.conn.closed:
                raise rpyc.ConnectionError("Connection is closed")
            # Check for responsiveness
            self.conn.ping()
        except Exception:
            self.conn = rpyc.connect("localhost", 18812)

    def get_connection(self):
        self.reconnect_if_needed()
        try:
            return self.conn.root.get_connected()
        except Exception as e:
            self.logger.error(f"Failed to call get_connected: {e}")
            return False


    def start_inner_server(self):
        service = VTSControlService(self.loop)
        self.inner_server = ThreadedServer(service, port=18812)
        print("RPC server thread started on port 18812")
        self.inner_server.start()

    def get_connected(self):
        self.get_connection()
        return self.conn.root.get_connected()

    def connect_auth(self):
        self.get_connection()
        return self.conn.root.connect_auth()

    def getHotkeys(self)->list[str]:
        self.get_connection()
        return self.conn.root.get_hotkeys()

    def triggerHotkey(self, hotkey: str)->bool:
        self.get_connection()
        return self.conn.root.trigger_hotkey(hotkey)

    def moveModel(self, x: float, y: float, rot: int, size: int, relative: bool, move_time: float)->bool:
        self.get_connection()
        return self.conn.root.move_model(x, y, rot, size, relative, move_time)

    def getModelPosition(self):
        self.get_connection()
        return self.conn.root.get_model_postion()

backend = Backend()

