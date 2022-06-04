from .config import *
import os

def curses_installed():
    return False

def print_banner():
    length = len(BANNER.split('\n')[0])
    total_length = os.get_terminal_size()[0]
    spaces = (total_length - length) // 2
    for line in BANNER.split('\n'):
        print(' ' * spaces + line)