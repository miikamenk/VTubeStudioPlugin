# Import StreamController modules
from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionHolder import ActionHolder

# Import VTS backend
from .VTubeStudio.backend.VTSController import VTSController

# Import actions
from .actions.TriggerHotkey.TriggerHotkey import TriggerHotkey
from .actions.Pan.Pan import Pan
from .actions.Zoom.Zoom import Zoom
from .actions.Rotate.Rotate import Rotate

class VTubeStudio(PluginBase):
    def __init__(self):
        super().__init__()
        self.vts = VTSController()

        ## Register actions
        self.trigger_hotkey_holder = ActionHolder(
            plugin_base = self,
            action_base = TriggerHotkey,
            action_id = "dev_miikamenk_Template::TriggerHotkey", # Change this to your own plugin id
            action_name = "Trigger Hotkey", 
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
                Input.Key: ActionInputSupport.UNTESTED,
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
                Input.Key: ActionInputSupport.UNTESTED,
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
                Input.Key: ActionInputSupport.UNTESTED,
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
