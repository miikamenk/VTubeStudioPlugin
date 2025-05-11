import asyncio
from rpyc.utils.server import ThreadedServer
from VtsController import VTSControlService  # This can safely use pyvts etc.

def main():
    service = VTSControlService()
    server = ThreadedServer(service, port=18812)
    print("VTS RPyC server started on port 18812")
    server.start()

if __name__ == "__main__":
    main()
