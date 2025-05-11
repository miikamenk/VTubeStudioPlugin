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
        icon_path = os.path.join(self.plugin_base.PATH, "assets", "zoom.png")
        self.set_media(media_path=icon_path, size=0.75)

        try:
            connected = self.plugin_base.get_connected()
            if not connected:
                log.info("Not connected. Make sure VTubeStudio api is running")
        except Exception as e:
            log.error(f"Error during connection/authentication process: {e}")


    def event_callback(self, event: InputEvent, data: dict = None):
        if event == Input.Key.Events.SHORT_UP:
            self.on_key_down()
        elif event == Input.Key.Events.HOLD_START or event == Input.Dial.Events.HOLD_START:
            self.on_key_hold_start()
        elif event == Input.Dial.Events.TURN_CW:
            self.on_dial_turn(+1)
        elif event == Input.Dial.Events.TURN_CCW:
            self.on_dial_turn(-1)
        elif event == Input.Dial.Events.SHORT_UP:
            self.on_key_down()
        
    def on_ready(self) -> None:
        self.on_tick()


    def on_key_down(self) -> None:
        settings = self.get_settings()
        pos = self.plugin_base.backend.getModelPosition()
        x = pos["x"]
        y = pos["y"]
        rot = pos["rot"]
        zoom = settings.get("size", 0)

        self.plugin_base.backend.moveModel(x, y, rot, zoom, False, 1)

    def on_key_hold_start(self) -> None:
        settings = self.get_settings()
        pos = self.plugin_base.backend.getModelPosition()
        x = pos["x"]
        y = pos["y"]
        rot = pos["rot"]
        zoom = settings.get("held_size", 0)

        self.plugin_base.backend.moveModel(x, y, rot, zoom, False, 1)

    def on_dial_turn(self, direction: int):
        try:
            settings = self.get_settings()
            amount = settings.get("amount", 0)
            move_time = 1.0

            delta = -amount if direction < 0 else amount

            # Relative move: just apply delta to zoom
            x, y, rot = 0, 0, 0
            zoom = delta

            self.plugin_base.backend.moveModel(x, y, rot, zoom, True, move_time)

        except Exception as e:
            log.error(e)
            self.show_error(1)
    
    def get_config_rows(self) -> list:
        self.amount_scale = ScaleRow(title=self.plugin_base.lm.get("actions.zoom.amount"), value=1, min=1, max=10, step=1, draw_value=True)
        self.size_scale = ScaleRow(title=self.plugin_base.lm.get("actions.zoom.size"), value=0, min=-100, max=100, step=5, draw_value=True)
        self.held_size_scale = ScaleRow(title=self.plugin_base.lm.get("actions.zoom.held_size"), value=0, min=-100, max=100, step=5, draw_value=True)

        self.amount_scale.scale.connect("value-changed", self.on_amount_change)
        self.size_scale.scale.connect("value-changed", self.on_size_change)
        self.held_size_scale.scale.connect("value-changed", self.on_held_size_change)

        self.load_config_settings()

        return [self.amount_scale, self.size_scale, self.held_size_scale]
 
    def load_config_settings(self):
        settings = self.get_settings()
        if settings == None:
            return
        self.amount_scale.scale.set_value(settings.get("amount", 1))
        self.size_scale.scale.set_value(settings.get("size", 0))
        self.held_size_scale.scale.set_value(settings.get("held_size", 0))
 
    def on_amount_change(self, scale, *args):
        settings = self.get_settings()

        amount = scale.get_value()

        ## self.display_info()

        settings["amount"] = amount
        self.set_settings(settings)

    def on_size_change(self, scale, *args):
        settings = self.get_settings()

        amount = scale.get_value()

        ## self.display_info()

        settings["size"] = amount
        self.set_settings(settings)

    def on_held_size_change(self, scale, *args):
        settings = self.get_settings()

        amount = scale.get_value()

        ## self.display_info()

        settings["held_size"] = amount
        self.set_settings(settings)

