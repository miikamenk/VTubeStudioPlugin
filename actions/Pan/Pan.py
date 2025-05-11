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

class Pan(ActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.has_configuration = True

    def on_tick(self):
        icon_path = os.path.join(self.plugin_base.PATH, "assets", "pan.png")
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
        x = settings.get("press_x")
        y = settings.get("press_y")
        rot = pos["rot"]
        zoom = pos["size"]
        move_time = settings.get("time", 0)

        x = max(-1000, min(1000, x))
        y = max(-1000, min(1000, y))
        rot = max(-360, min(360, rot))
        zoom = max(-100, min(100, zoom))

        self.plugin_base.backend.moveModel(x, y, rot, zoom, False, move_time)

    def on_key_hold_start(self) -> None:
        settings = self.get_settings()
        pos = self.plugin_base.backend.getModelPosition()
        x = settings.get("held_x")
        y = settings.get("held_y")
        rot = pos["rot"] 
        zoom = pos["size"]
        move_time = settings.get("time", 0)

        x = max(-1000, min(1000, x))
        y = max(-1000, min(1000, y))
        rot = max(-360, min(360, rot))
        zoom = max(-100, min(100, zoom))

        self.plugin_base.backend.moveModel(x, y, rot, zoom, False, move_time)

    def on_dial_turn(self, direction: int):
        try:
            settings = self.get_settings()
            amount_x = settings.get("x", 0)
            amount_y = settings.get("y", 0)
            move_time = settings.get("time", 0)

            delta_x = -amount_x if direction < 0 else amount_x
            delta_y = -amount_y if direction < 0 else amount_y

            # Relative move: just apply delta to zoom
            rot, zoom = 0, 0

            self.plugin_base.backend.moveModel(delta_x, delta_y, rot, zoom, True, move_time)
        except Exception as e:
            log.error(e)
            self.show_error(1)
    
    def get_config_rows(self) -> list:
        self.x_scale = ScaleRow(title=self.plugin_base.lm.get("actions.pan.x"), value=0, min=-1, max=1, step=0.05, draw_value=True)
        self.y_scale = ScaleRow(title=self.plugin_base.lm.get("actions.pan.y"), value=0, min=-1, max=1, step=0.05, draw_value=True)
        self.press_x_scale = ScaleRow(title=self.plugin_base.lm.get("actions.pan.press_x"), value=0, min=-2, max=2, step=0.1, draw_value=True)
        self.press_y_scale = ScaleRow(title=self.plugin_base.lm.get("actions.pan.press_y"), value=0, min=-2, max=2, step=0.1, draw_value=True)
        self.held_x_scale = ScaleRow(title=self.plugin_base.lm.get("actions.pan.held_x"), value=0, min=-2, max=2, step=0.1, draw_value=True)
        self.held_y_scale = ScaleRow(title=self.plugin_base.lm.get("actions.pan.held_y"), value=0, min=-2, max=2, step=0.1, draw_value=True)
        self.time_scale = ScaleRow(title=self.plugin_base.lm.get("plugin.time"), value=0, min=0, max=2, step=0.25, draw_value=True)

        self.x_scale.scale.connect("value-changed", self.on_x_change)
        self.y_scale.scale.connect("value-changed", self.on_y_change)
        self.press_x_scale.scale.connect("value-changed", self.on_press_x_change)
        self.press_y_scale.scale.connect("value-changed", self.on_press_y_change)
        self.held_x_scale.scale.connect("value-changed", self.on_held_x_change)
        self.held_y_scale.scale.connect("value-changed", self.on_held_y_change)
        self.time_scale.scale.connect("value-changed", self.on_time_change)

        self.load_config_settings()

        return [self.x_scale, self.y_scale, self.press_x_scale, self.press_y_scale, self.held_x_scale, self.held_y_scale, self.time_scale]
 
    def load_config_settings(self):
        settings = self.get_settings()
        if settings == None:
            return
        self.x_scale.scale.set_value(settings.get("x", 0))
        self.y_scale.scale.set_value(settings.get("y", 0))
        self.press_x_scale.scale.set_value(settings.get("press_x", 0))
        self.press_y_scale.scale.set_value(settings.get("press_y", 0))
        self.held_x_scale.scale.set_value(settings.get("held_x", 0))
        self.held_y_scale.scale.set_value(settings.get("held_y", 0))
        self.time_scale.scale.set_value(settings.get("time", 0))
 
    def on_x_change(self, scale, *args):
        settings = self.get_settings()

        amount = scale.get_value()

        ## self.display_info()

        settings["x"] = amount
        self.set_settings(settings)

    def on_y_change(self, scale, *args):
        settings = self.get_settings()

        amount = scale.get_value()

        ## self.display_info()

        settings["y"] = amount
        self.set_settings(settings)

    def on_press_x_change(self, scale, *args):
        settings = self.get_settings()

        amount = scale.get_value()

        ## self.display_info()

        settings["press_x"] = amount
        self.set_settings(settings)

    def on_press_y_change(self, scale, *args):
        settings = self.get_settings()

        amount = scale.get_value()

        ## self.display_info()

        settings["press_y"] = amount
        self.set_settings(settings)

    def on_held_x_change(self, scale, *args):
        settings = self.get_settings()

        amount = scale.get_value()

        ## self.display_info()

        settings["held_x"] = amount
        self.set_settings(settings)

    def on_held_y_change(self, scale, *args):
        settings = self.get_settings()

        amount = scale.get_value()

        ## self.display_info()

        settings["held_y"] = amount
        self.set_settings(settings)

    def on_time_change(self, scale, *args):
        settings = self.get_settings()

        amount = scale.get_value()

        ## self.display_info()

        settings["time"] = amount
        self.set_settings(settings)
