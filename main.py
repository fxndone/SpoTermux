#!/usr/bin/python3

from core.play_music import *
from core.versions import *
from core.screen import *
from core.io import *

import threading
import random
import sys
import os


directory = "musics/"

if len(sys.argv) > 1:
    if os.path.isdir(sys.argv[1]):
        directory = sys.argv[1]

if check_for_updates():
    sys.exit(0)

iface = curses_installed()

player = Player()

if not iface:
    clear_screen()

    print("[+] Starting SpoTermux...")
    print("[+] You should consider installing curses !")

    print('\n' * 3)

    print_banner()

    stop = threading.Event()
    threading.Thread(target=InputManager, args=(player, directory, stop), daemon=True).start()

    while not stop.is_set():
        if not player.check_play():
            nxt = random.choice(os.listdir(directory))
            while nxt == player.last:
                nxt = random.choice(os.listdir(directory))
            player.run(os.path.join(directory, nxt))