import pyvts
import asyncio

plugin_info = {
    "plugin_name": "Stream-controller VTS",
    "developer": "miikamenk",
    "authentication_token_path": "./pyvts_token.txt"
}

class VTSController():
    def __init__(self):
        self.vts = pyvts.vts(plugin_info=plugin_info)

    def get_connected(self):
        auth_status = self.vts.get_authentic_status()
        if auth_status == 2:
            return True
        else:
            return False

    async def connect_auth(self):
        await self.vts.connect()
        await self.vts.request_authenticate_token()
        await self.vts.request_authenticate()
        await self.vts.close()

    async def getHotkeys(self)->list[str]:
        await self.vts.connect()
        await self.vts.request_authenticate()
        response_data = await self.vts.request(self.vts.vts_request.requestHotKeyList())
        hotkey_list = []
        for hotkey in response_data['data']['availableHotkeys']:
            hotkey_list.append(hotkey['name'])
        await self.vts.close()
        return hotkey_list 

    async def triggerHotkey(self, hotkey: str)->bool:
        await self.vts.connect()
        await self.vts.request_authenticate()

        request = await self.vts.request(self.vts.vts_request.requestTriggerHotKey(hotkey))

        await self.vts.close()
        print(request)
        return True

    async def moveModel(self, x: float, y: float, rot: int, size: int, relative: bool, move_time: float)->bool:
        await self.vts.connect()
        await self.vts.request_authenticate()
        request_data = self.vts.vts_request.requestMoveModel(x, y, rot, size, relative, move_time)

        request = await self.vts.request(request_data)

        await self.vts.close()
        print(request)
        return True

    async def getModelPosition(self):
        await self.vts.connect()
        await self.vts.request_authenticate()

        # Send a CurrentModelRequest to get model info
        response = await self.vts.request({
            "messageType": "CurrentModelRequest"
        })

        if response["data"].get("modelLoaded"):
            position = response["data"].get("modelPosition", [0.0, 0.0, 0.0, 0.0])
            result = {
                "x": position[0],
                "y": position[1],
                "rotation": position[2],
                "size": position[3]
            }        
        else:
            result = {
                "x": 0.0,
                "y": 0.0,
                "rotation": 0.0,
                "size": 1.0
            }
            print("No model is currently loaded.")

        await self.vts.close()
        return result

