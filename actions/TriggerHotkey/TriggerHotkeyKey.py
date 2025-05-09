# Import StreamController modules
from src.backend.PluginManager.ActionBase import ActionBase
from src.backend.DeckManagement.DeckController import DeckController
from src.backend.PageManagement.Page import Page
from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.DeckManagement.InputIdentifier import Input, InputEvent, InputIdentifier

# Import python modules
import os
from loguru import logger as log

# Import gtk modules - used for the config rows
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import GObject, Gtk, Adw

class TriggerHotkeyKey(ActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.has_configuration = True

    def on_tick(self):
        icon_path = os.path.join(self.plugin_base.PATH, "assets", "info.png")
        self.set_media(media_path=icon_path, size=0.75)

        try:
            connected = self.plugin_base.get_connected()
            if not connected:
                log.info("Not connected. Make sure VTubeStudio api is running")
        except Exception as e:
            log.error(f"Error during connection/authentication process: {e}")
        
    def on_ready(self) -> None:
        self.on_tick()

    def on_key_down(self) -> None:
        settings = self.get_settings()
        hotkey = settings.get("hotkey")
        self.plugin_base.backend.triggerHotkey(hotkey)
    
    def get_config_rows(self) -> list:
        self.hotkey_model = Gtk.StringList() # Hotkey 
        self.hotkey_row = Adw.ComboRow(title=self.plugin_base.lm.get("actions.trigger_hotkey.hotkey"), model=self.hotkey_model)
        self.hotkey_row.set_enable_search(True)

        self.load_hotkey_model()

        self.hotkey_row.connect("notify::selected-item", self.on_hotkey_change)

        self.load_config_settings()

        return [self.hotkey_row]
 
    def load_hotkey_model(self):
        hotkeys = self.plugin_base.backend.getHotkeys()
        for i in range(self.hotkey_model.get_n_items()):
            self.hotkey_model.remove(0)
        for hotkey in hotkeys:
            self.hotkey_model.append(hotkey)

 
    def load_config_settings(self):
        settings = self.get_settings()
        if settings == None:
            return
        hotkey = settings.get("hotkey")
        for i, device in enumerate(self.hotkey_model):
            if device == hotkey:
                self.hotkey_row.combo_box.set_active(i)
                break
 
    def on_hotkey_change(self, combo, *args):
        hotkey = combo.get_selected_item().get_string()

        settings = self.get_settings()
        settings["hotkey"] = hotkey 

        self.set_settings(settings)
