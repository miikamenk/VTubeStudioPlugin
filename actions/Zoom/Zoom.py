# Import StreamController modules
from src.backend.PluginManager.ActionBase import ActionBase
from src.backend.DeckManagement.DeckController import DeckController
from src.backend.PageManagement.Page import Page
from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.DeckManagement.InputIdentifier import Input, InputEvent, InputIdentifier

# Import python modules
import os
from loguru import logger as log

from GtkHelper.ScaleRow import ScaleRow

# Import gtk modules - used for the config rows
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import GObject, Gtk, Adw

class Zoom(ActionBase):
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
        current_pos = self.plugin_base.backend.getModelPosition()
        amount = settings.get("amount")
        relative = settings.get("relative")
        move_time = 1.0
        self.plugin_base.backend.moveModel(current_pos["x"], current_pos["y"], current_pos["rot"], amount, relative, move_time)

    def on_dial_turn(self, direction: int):
        try:
            settings = self.get_settings()
            amount = settings.get("amount", 0)
            relative = settings.get("relative", False)
            move_time = 1.0

            delta = -amount if direction < 0 else amount

            if relative:
                # Relative move: just apply delta to zoom
                x, y, rot = 0, 0, 0
                zoom = delta
            else:
                # Absolute move: keep current pos, apply zoom offset
                pos = self.plugin_base.backend.getModelPosition()
                x = pos.get("x", 0)
                y = pos.get("y", 0)
                rot = pos.get("rot", 0)
                zoom = pos.get("zoom", 1) + delta

            self.plugin_base.backend.moveModel(x, y, rot, zoom, relative, move_time)

        except Exception as e:
            log.error(e)
            self.show_error(1)
    
    def get_config_rows(self) -> list:
        self.relative_switch = Adw.SwitchRow(title=self.plugin_base.lm.get("actions.zoom.relative"))        
        self.amount_scale = ScaleRow(title=self.plugin_base.lm.get("actions.zoom.relative"), value=1, min=1, max=10, step=1)

        self.load_zoom_model()

        self.amount_scale.scale.connect("value-changed", self.on_amount_change)
        self.relative_switch.connect("notify::active", self.on_relative_switch_change)

        self.load_config_settings()

        return [self.zoom_row]
 
    def load_zoom_model(self):
        zooms = self.plugin_base.backend.getHotkeys()
        for i in range(self.zoom_model.get_n_items()):
            self.zoom_model.remove(0)
        for zoom in hotkeys:
            self.zoom_model.append(hotkey)

 
    def load_config_settings(self):
        settings = self.get_settings()
        if settings == None:
            return
        zoom = settings.get("hotkey")
        for i, device in enumerate(self.zoom_model):
            if device == zoom:
                self.zoom_row.combo_box.set_active(i)
                break
 
    def on_amount_change(self, combo, *args):
        settings = self.get_settings()

        amount = self.amount_scale.scale.get_value()

        ## self.display_info()

        settings["amount"] = amount
        self.set_settings(settings)

    def on_relative_switch_change(self, switch, *args):
        settings = self.get_settings()
        settings["relative"] = switch.get_active()
        self.set_settings(settings)
