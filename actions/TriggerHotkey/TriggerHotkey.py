# Import StreamController modules
from src.backend.PluginManager.ActionBase import ActionBase
from src.backend.DeckManagement.DeckController import DeckController
from src.backend.PageManagement.Page import Page
from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.DeckManagement.InputIdentifier import Input, InputEvent, InputIdentifier

# Import python modules
import os
import asyncio

# Import gtk modules - used for the config rows
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import GObject, Gtk, Adw

class TriggerHotkey(ActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.has_configuration = True

    def on_tick(self):
        print("here")
        
    def on_ready(self) -> None:
        icon_path = os.path.join(self.plugin_base.PATH, "assets", "info.png")
        self.set_media(media_path=icon_path, size=0.75)
        
    def on_key_down(self) -> None:
        settings = self.get_settings()
        hotkey = settings.get("hotkey")
        self.plugin_base.backend.triggerHotkey(hotkey)
    
    def get_config_rows(self) -> list:
        self.hotkey_model = Gtk.StringList() # Hotkey 
        self.hotkey_row = Adw.ComboRow(title=self.plugin_base.lm.get("actions.trigger_hotkey.hotkey"), model=self.hotkey_model)
        self.hotkey_row.set_enable_search(True)

        self.load_hotkey_model()

        self.hotkey_row.combo_box.connect("changed", self.on_hotkey_change)

        self.load_config_settings()

        return [self.hotkey_row]
 
    def load_hotkey_model(self):
        for i in range(self.hotkey_model.get_n_items()):
            self.hotkey_model.remove(0)

        
        with self.plugin_base.backend.getHotkeys() as hotkeys:
            for hotkey in hotkeys:
                self.hotkey_model.append(hotkey)

 
    def load_config_settings(self):
        settings = self.get_settings()
        hotkey = settings.get("hotkey")
        for i, device in enumerate(self.device_model):
            if device[0] == hotkey:
                self.device_row.combo_box.set_active(i)
                break
 
    def on_hotkey_change(self, combo_box, *args):
        hotkey = self.device_model[combo_box.get_active()][0]

        settings = self.get_settings()
        settings["hotkey"] = hotkey 

        self.set_settings(settings)

