# Import StreamController modules
from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionHolder import ActionHolder
from src.backend.DeckManagement.InputIdentifier import Input
from src.backend.PluginManager.ActionInputSupport import ActionInputSupport

import sys
import os
from loguru import logger as log
import time

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

        print("Launch backend")
        self.launch_backend(
            os.path.join(self.PATH, "VTubeStudio", "backend.py"),
            os.path.join(self.PATH, "VTubeStudio", ".venv"),
            open_in_terminal=True
        )

        
  
        self.lm = self.locale_manager

        ## Register actions
        self.trigger_hotkey_holder = ActionHolder(
            plugin_base = self,
            action_base = TriggerHotkey,
            action_id = "dev_miikamenk_Template::TriggerHotkey", # Change this to your own plugin id
            action_name = self.lm.get("actions.trigger_hotkey.name"),
            action_support={
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.UNTESTED,
                Input.Touchscreen: ActionInputSupport.UNTESTED
            }
        )
        self.add_action_holder(self.trigger_hotkey_holder)

        self.pan_holder = ActionHolder(
            plugin_base = self,
            action_base = Pan,
            action_id = "dev_miikamenk_Template::Pan",
            action_name = "Pan",
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
            action_id = "dev_miikamenk_Template::Zoom",
            action_name = "Zoom",
            action_support={
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.SUPPORTED,
                Input.Touchscreen: ActionInputSupport.UNTESTED
            }
        )
        self.add_action_holder(self.zoom_holder)

        self.rotate_holder = ActionHolder(
            plugin_base = self,
            action_base = Rotate,
            action_id = "dev_miikamenk_Template::Rotate",
            action_name = "Rotate",
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
            plugin_version = "0.0.1",
            app_version = "1.1.1-alpha"
        )

    def get_connected(self):
        try:
            return self.backend.connect_auth()
        except Exception as e:
            log.error(e)
            return False
