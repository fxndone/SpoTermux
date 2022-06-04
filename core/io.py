from .commands import *
from .screen import *
from .utils import *

import readline
import random
import os

COMMANDS = ["clear", "exit", "pass", "play", "pause", "back", "list", "repeat", "up", "down", "len", "queue ", "quit", "refresh", "ls", "current", "infos"]
COMMANDS_BCKP = COMMANDS[:]

def complete(text, state):
    for cmd in COMMANDS:
        if cmd.startswith(text):
            if not state:
                return cmd
            else:
                state -= 1

def InputManager(player, directory, event):
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete)

    musics = os.listdir(directory)

    for music in musics:
        COMMANDS.append(music)

    while 1:
        ch = input()
        for chx in ch.split(';'):
            if os.path.isfile(os.path.join(directory, chx)):
                player.run(os.path.join(directory, chx))
            elif cleared_string(chx) == "pass":
                player.run(os.path.join(directory, random.choice(musics)))
            elif cleared_string(chx) == "clear":
                clear_screen()
                print_banner()
            elif cleared_string(chx) == "back":
                if player.last != None:
                    player.run(os.path.join(directory, player.last))
            elif cleared_string(chx) in ("quit", "exit"):
                event.set()
                return
            elif cleared_string(chx) in ("list", "ls"):
                print('\n'.join(sorted(musics)))