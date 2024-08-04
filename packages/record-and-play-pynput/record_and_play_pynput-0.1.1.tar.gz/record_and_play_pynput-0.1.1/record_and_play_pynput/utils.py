"""This module stores common utility functions for the project."""

# Built-in modules
import argparse
import json

def read_json_file(filepath):
    """
    This function reads a JSON file and returns its contents as a dictionary.
    It handles common exceptions that may occur when reading a file.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        print(f"Error: The file {filepath} does not exist.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file {filepath} is not a valid JSON file.")
        return None
    except PermissionError:
        print(f"Error: Permission denied when trying to read the file {filepath}.")
        return None
    except OSError as e:
        print(f"OS error occurred: {e}")
        return None
