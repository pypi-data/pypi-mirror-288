"""This module is used to play the recording of the user's actions."""

# Built-in modules
import argparse
import time

# Third-party modules
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Controller as KeyboardController

# Local modules
from record_and_play_pynput.config import config
from record_and_play_pynput.utils import read_json_file

# Initialize keyboard and mouse controllers
keyboard = KeyboardController()
mouse = MouseController()

def parse_arguments():
    parser = argparse.ArgumentParser(description="Play the user's recording.")
    parser.add_argument("-n", "--name_of_recording", type=str, help="Name of the recording (without .txt).")
    parser.add_argument("-p", "--plays", type=int, help="Number of times to play the recording.")
    return parser.parse_args()

def play_key_action(action: str, key: str) -> None:
    """This function plays the key action."""
    if action == "pressed_key":
        keyboard.press(key)
    else:
        keyboard.release(key)

def play_mouse_action(action: str, x: int, y: int, button: str=None,
                      horizontal_direction: int=0, vertical_direction: int=0):
    """This function plays the mouse action."""
    mouse.position = (x, y)
    if action == "pressed":
        mouse.press(Button.left if button == "Button.left" else Button.right)
    elif action == "released":
        mouse.release(Button.left if button == "Button.left" else Button.right)
    elif action == "scroll":
        mouse.scroll(horizontal_direction, vertical_direction)

def get_pause_time(data: list, index: int, current_time: float) -> float:
    """This function calculates the pause time between actions."""
    try:
        next_movement = data[index + 1]['event_time']
        pause_time = next_movement - current_time
        return pause_time
    except IndexError:
        return 1

def should_move_for_action(data: list, index: int, action: str, x: int, y: int) -> bool:
    """This function determines if the mouse should move for the action."""
    if action in ["pressed", "released", "scroll"] and index > 0 and data[index - 1]['action'] not in ["pressed_key", "released_key"]:
        prev_x, prev_y = data[index - 1]['x'], data[index - 1]['y']
        if x == prev_x and y == prev_y:
            return False
    return True

def main(args=None):
    """This function plays the user's recording."""

    if args is None:
        args = parse_arguments()
    
    name_of_recording = f"data/{args.name_of_recording}.json"
    number_of_plays = args.plays

    # Read the JSON recording file and store its contents in a dictionary.
    data = read_json_file(name_of_recording)

    for _ in range(number_of_plays):
        for index, item in enumerate(data):
            action, current_time = item['action'], item['event_time']
            pause_time = get_pause_time(data, index, current_time)

            if action in ["pressed_key", "released_key"]:
                key = item['key'] if 'Key.' not in item['key'] else config.special_keys[item['key']]
                print(f"action: {action}, time: {current_time}, key: {key}")
                play_key_action(action, key)
            else:
                x, y = item['x'], item['y']
                move_for_action = should_move_for_action(data, index, action, x, y)
                print(f"x: {x}, y: {y}, action: {action}, time: {current_time}")

                if move_for_action:
                    # Small delay before performing the action.
                    time.sleep(0.001)

                play_mouse_action(action, x, y, item.get("button"),
                                  item.get("horizontal_direction", 0),
                                  item.get("vertical_direction", 0))

            time.sleep(pause_time)

if __name__ == "__main__":
    main()
