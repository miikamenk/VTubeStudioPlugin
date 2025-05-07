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

        request = await self.vts.request(self.vts.vts_request.requestTriggerHotkey(hotkey))

        await self.vts.close()
        print(request)
        return True

    async def moveModel(self, x: float, y: float, rot: float, size: float, relative: bool, move_time: float)->bool:
        await self.vts.connect()
        await self.vts.request_authenticate()
        request_data = self.vts.vts_request.requestMoveModel(x, y, rot, size, relative, move_time)

        request = await self.vts.request(request_data)

        await self.vts.close()
        print(request)
        return True

