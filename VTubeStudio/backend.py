import pyvts
import asyncio

plugin_info = {
    "plugin_name": "Stream-controller VTS",
    "developer": "miikamenk",
    "authentication_token_path": "./pyvts_token.txt"
}

class VTSController():
    async def __init__(self):
        self.vts = pyvts.vts(plugin_info=plugin_info):

    async def connect_auth():
        await vts.connect()
        await vts.request_authenticate_token()
        await vts.request_authenticate()
        await vts.close()

    async def getHotkeys()->str[]:
        await vts.connect()
        await vts.request_authenticate()
        response_data = await myvts.request(myvts.vts_request.requestHotKeyList())
        hotkey_list = []
        for hotkey in response_data['data']['availableHotkeys']:
            hotkey_list.append(hotkey['name'])
        await vts.close()
        return hotkey_list 

    async def triggerHotkey(hotkey: str)->bool:
        await vts.connect()
        await vts.request_authenticate()

        request = await vts.request(vts.vts_request.requestTriggerHotkey(hotkey))

        await vts.close()
        print(request)
        return True

    async def moveModel(x: float, y: float, rot: float, size: float, relative: bool, move_time: float)->bool:
        await vts.connect()
        await vts.request_authenticate()
        request_data = await vts.vts_request.requestMoveModel(x, y, rot, size, relative, move_time)

        request = await vts.request(request_data)

        await vts.close()
        print(request)
        return True

