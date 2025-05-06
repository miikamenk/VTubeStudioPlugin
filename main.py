# Import StreamController modules
from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionHolder import ActionHolder

# Import actions
from .actions.SimpleAction.SimpleAction import SimpleAction

class VTubeStudio(PluginBase):
    def __init__(self):
        super().__init__()

        ## Register actions
        self.trigger_hotkey_holder = ActionHolder(
            plugin_base = self,
            action_base = SimpleAction,
            action_id = "dev_miikamenk_Template::TriggerHotkey", # Change this to your own plugin id
            action_name = "Trigger Hotkey",
        )
        self.add_action_holder(self.trigger_hotkey_holder)

        self.pan_holder = ActionHolder(
            plugin_base = self,
            action_base = SimpleAction,
            action_id = "dev_miikamenk_Template::Pan",
            action_name = "Pan",
        )
        self.add_action_holder(self.pan_holder)

        self.zoom_holder = ActionHolder(
            plugin_base = self,
            action_base = SimpleAction,
            action_id = "dev_miikamenk_Template::Zoom",
            action_name = "Zoom",
        )
        self.add_action_holder(self.simple_action_holder)

        self.rotate_holder = ActionHolder(
            plugin_base = self,
            action_base = SimpleAction,
            action_id = "dev_miikamenk_Template::Rotate",
            action_name = "Rotate",
        )
        self.add_action_holder(self.rotate_holder)

        # Register plugin
        self.register(
            plugin_name = "VTubeStudio",
            github_repo = "https://github.com/miikamenk/com_miikamenk_VTubeStudio",
            plugin_version = "0.0.1",
            app_version = "1.1.1-alpha"
        )
