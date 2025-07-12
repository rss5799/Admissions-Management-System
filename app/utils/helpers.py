import sys
import os

def filter_dict(data: dict) -> dict:
    """
    Filters out the 'csrf_token' key from a dictionary.
    
    Returns:
        A function that takes a dictionary and returns a new dictionary without the 'csrf_token' key.
    """
    filtered_data = {k: v for k, v in data.items() if k != 'csrf_token'}

    return filtered_data

def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller
    """
    if getattr(sys, 'frozen', False):
        # Running in a PyInstaller bundle
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)