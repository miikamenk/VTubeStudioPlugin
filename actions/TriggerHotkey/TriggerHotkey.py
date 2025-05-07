# Import StreamController modules
from src.backend.PluginManager.ActionBase import ActionBase
from src.backend.DeckManagement.DeckController import DeckController
from src.backend.PageManagement.Page import Page
from src.backend.PluginManager.PluginBase import PluginBase

# Import python modules
import os
import asyncio

# Import gtk modules - used for the config rows
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

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
        asyncio.create_task(self.vts.triggerHotkey(hotkey))
    
    def get_config_rows(self) -> list:
        self.hotkey_model = Gtk.ListStore.new([str]) # Hotkey 
        self.hotkey_row = ComboRow(title=self.plugin_base.lm.get("actions.trigger_hotkey.hotkey"), model=self.hotkey_model)

        self.hotkey_cell_renderer = Gtk.CellRendererText()
        self.hotkey_row.combo_box.pack_start(self.hotkey_cell_renderer, True)
        self.hotkey_row.combo_box.add_attribute(self.hotkey_cell_renderer, "text", 0)

        self.load_hotkey_model()

        self.hotkey_row.combo_box.connect("changed", self.on_hotkey_change)

        return [self.hotkey_row]
 
    async def load_hotkey_model(self):
        self.hotkey_model.clear()
        
        with await vts.getHotkeys() as hotkeys:
            for hotkey in hotkeys:
                self.hotkey_model.append([hotkey])

        self.load_config_settings()
 
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

