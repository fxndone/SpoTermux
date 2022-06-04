from .config import *

def cleared_string(string, aviables="abcdefghijklmnopqrstuvwxyz0123456789.:!_-()"):
    return ''.join([char for char in string if char.lower() in aviables])