"""This module is used to record the user's actions."""

# Built-in modules
import argparse
import json
import time
from typing import Union

# Third-party modules
from pynput import mouse
from pynput import keyboard
from functools import partial

# Global storage for events
storage = []

def parse_arguments():
    parser = argparse.ArgumentParser(description="Record mouse and keyboard actions.")
    parser.add_argument("-n", "--name_of_recording", type=str, help="Name of the recording (without .txt).")
    return parser.parse_args()

def save_recording(name_of_recording: str) -> None:
    """This function names and saves the recording to a .txt file."""
    with open(f"data/{name_of_recording}.json", "w") as outfile:
        json.dump(storage, outfile)

def on_press(key: Union[keyboard.Key, keyboard.KeyCode]) -> Union[None, bool]:
    """
    This function is called when a key is pressed. It appends the action to the recording file.
    If the key is 'esc', it stops the recording.
    """
    try:
        action_item = {'action':'pressed_key', 'key':key.char, 'event_time': time.time()}
    except AttributeError:
        # Here we want to check whether the key is 'esc' and return False if it is.
        # This will stop the recording. If not it is another special key and we will add it.
        if key == keyboard.Key.esc:
            return False
        action_item = {'action':'pressed_key', 'key':str(key), 'event_time': time.time()}
    storage.append(action_item)

def on_release(key: Union[keyboard.Key, keyboard.KeyCode]) -> None:
    """This function is called when a key is released. It appends the action to the recording file."""
    try:
        action_item = {'action':'released_key', 'key':key.char, 'event_time': time.time()}
    except AttributeError:
        action_item = {'action':'released_key', 'key':str(key), 'event_time': time.time()}
    storage.append(action_item)

def on_move(x: int, y: int) -> None:
    """
    This function appends mouse movement to the recording file.
    """
    action_item = {'action': 'moved', 'x': x, 'y': y, 'event_time': time.time()}
    storage.append(action_item)

def on_click(x: int, y: int, button: mouse.Button, pressed: bool, name_of_recording: str) -> Union[None, bool]:
    action_item = {'action': 'pressed' if pressed else 'released', 'button': str(button), 'x': x, 'y': y, 'event_time': time.time()}
    storage.append(action_item)
    # Here we want to check whether the right button was pressed for more than 2 seconds and then released.
    # If so we will save the recording and return False to stop the recording.
    if len(storage) > 1 and not pressed:
        if storage[-1]['action'] == 'released' and storage[-1]['button'] == 'Button.right' and storage[-1]['event_time'] - storage[-2]['event_time'] > 2:
            save_recording(name_of_recording)
            return False

def on_scroll(x: int, y: int, dx: int, dy: int) -> None:
    action_item = {'action': 'scroll', 'vertical_direction': int(dy), 'horizontal_direction': int(dx),
                   'x': x, 'y': y, 'event_time': time.time()}
    storage.append(action_item)

def main(args=None):
    """This function records the user's keyboard and mouse actions."""
    
    if args is None:
        args = parse_arguments()
    
    name_of_recording = args.name_of_recording
    
    print(f"Recording name: {name_of_recording}")
    print("Hold right click for more than 2 seconds (and then release) to end the recording for mouse and click 'esc' to end the recording for keyboard (both are needed to finish recording)")

    # Collect events from keyboard until esc
    # Collect events from mouse until right click for more than 2 seconds
    keyboard_listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)

    mouse_listener = mouse.Listener(
            on_click=partial(on_click, name_of_recording=name_of_recording),
            on_scroll=on_scroll,
            on_move=on_move)

    try:
        keyboard_listener.start()
        mouse_listener.start()
        keyboard_listener.join()
        mouse_listener.join()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        keyboard_listener.stop()
        mouse_listener.stop()

if __name__ == "__main__":  
    main()
