"""This module acts as a configuration file for the project."""

# Third-party modules
from pynput.keyboard import Key

class Config:
    """This class is used to store the configuration of the project."""
    def __init__(self):

        self.special_keys = {
            "Key.shift": Key.shift, "Key.tab": Key.tab, "Key.caps_lock": Key.caps_lock, 
            "Key.ctrl": Key.ctrl, "Key.alt": Key.alt, "Key.cmd": Key.cmd, 
            "Key.cmd_r": Key.cmd_r, "Key.alt_r": Key.alt_r, "Key.ctrl_r": Key.ctrl_r, 
            "Key.shift_r": Key.shift_r, "Key.enter": Key.enter, 
            "Key.backspace": Key.backspace, "Key.f19": Key.f19, "Key.f18": Key.f18, 
            "Key.f17": Key.f17, "Key.f16": Key.f16, "Key.f15": Key.f15, "Key.f14": Key.f14, 
            "Key.f13": Key.f13, "Key.media_volume_up": Key.media_volume_up, 
            "Key.media_volume_down": Key.media_volume_down, 
            "Key.media_volume_mute": Key.media_volume_mute, 
            "Key.media_play_pause": Key.media_play_pause, "Key.f6": Key.f6, 
            "Key.f5": Key.f5, "Key.right": Key.right, "Key.down": Key.down, 
            "Key.left": Key.left, "Key.up": Key.up, "Key.page_up": Key.page_up, 
            "Key.page_down": Key.page_down, "Key.home": Key.home, "Key.end": Key.end, 
            "Key.delete": Key.delete, "Key.space": Key.space
        }

# Create an instance of the Config class to import throughout the project.
config = Config()
