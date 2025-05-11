# Import StreamController modules
from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionHolder import ActionHolder
from src.backend.DeckManagement.InputIdentifier import Input
from src.backend.PluginManager.ActionInputSupport import ActionInputSupport

import sys
import os
from loguru import logger as log

# Add plugin to sys.paths
sys.path.append(os.path.dirname(__file__))

# Import actions
from .actions.TriggerHotkey.TriggerHotkey import TriggerHotkey
from .actions.Pan.Pan import Pan
from .actions.Zoom.Zoom import Zoom
from .actions.Rotate.Rotate import Rotate


class VTubeStudio(PluginBase):
    def __init__(self):
        super().__init__()
        self.auth = False
        self.auth_lock = False
        self.auth_limit = 3
        self.auth_counter = 0

        print("Launch backend")
        self.launch_backend(
            os.path.join(self.PATH, "VTubeStudio", "backend.py"),
            os.path.join(self.PATH, "VTubeStudio", ".venv"),
            open_in_terminal=False
        )

        self.lm = self.locale_manager

        ## Register actions
        self.trigger_hotkey_holder = ActionHolder(
            plugin_base = self,
            action_base = TriggerHotkey,
            action_id = "com_miikamenk_vtubestudio::TriggerHotkey", # Change this to your own plugin id
            action_name = self.lm.get("actions.trigger_hotkey.name"),
            action_support={
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.UNSUPPORTED,
                Input.Touchscreen: ActionInputSupport.UNTESTED
            }
        )
        self.add_action_holder(self.trigger_hotkey_holder)

        self.pan_holder = ActionHolder(
            plugin_base = self,
            action_base = Pan,
            action_id = "com_miikamenk_vtubestudio::Pan",
            action_name = self.lm.get("actions.pan.name"),
            action_support={
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.SUPPORTED,
                Input.Touchscreen: ActionInputSupport.UNTESTED
            }
        )
        self.add_action_holder(self.pan_holder)

        self.zoom_holder = ActionHolder(
            plugin_base = self,
            action_base = Zoom,
            action_id = "com_miikamenk_vtubestudio::Zoom",
            action_name = self.lm.get("actions.zoom.name"),
            action_support={
                Input.Key: ActionInputSupport.UNSUPPORTED,
                Input.Dial: ActionInputSupport.SUPPORTED,
                Input.Touchscreen: ActionInputSupport.UNTESTED
            }
        )
        self.add_action_holder(self.zoom_holder)

        self.rotate_holder = ActionHolder(
            plugin_base = self,
            action_base = Rotate,
            action_id = "com_miikamenk_vtubestudio::Rotate",
            action_name = self.lm.get("actions.rotate.name"),
            action_support={
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.SUPPORTED,
                Input.Touchscreen: ActionInputSupport.UNTESTED
            }
        )
        self.add_action_holder(self.rotate_holder)

        # Register plugin
        self.register(
            plugin_name = "VTubeStudio",
            github_repo = "https://github.com/miikamenk/com_miikamenk_VTubeStudio",
            plugin_version = "1.0.0",
            app_version = "1.5.0-beta.10"
        )

    def get_connected(self, force = False):
        try:
            if not self.auth_lock:
                if not self.auth or force:
                    self.backend.connect_auth()
                    connected = self.backend.get_connected()
                    self.auth = connected 
                    if connected:
                        self.auth_counter = 0
                        return connected
                    else: 
                        if self.auth_limit >= self.auth_counter:
                            self.auth_counter += 1
                        else:
                            self.auth_lock = True
            return False
        except Exception as e:
            self.auth = False
            if self.auth_limit >= self.auth_counter:
                self.auth_counter += 1
            else:
                self.auth_lock = True
            log.error(e)
            return False

