#!/usr/bin/python3

from os import system, listdir, remove, get_terminal_size as gts
from os.path import isfile, abspath, isdir
from random import choice, shuffle
from threading import Thread
from time import sleep
from json import load

import readline
import sys

last     = ""
queue    = []
play     = True
xit      = False
repeat   = False
index    = 0

ACTIONS  = ["clear", "exit", "banner", "pass", "play", "pause", "back", "list", "repeat", "unrepeat", "up", "down", "len", "queue ", "quit", "refresh", "ls", "current", "infos"]
COMMANDS = ACTIONS[:]

def getSounds(x=None):
	if x == None:
		ls = listdir(ARG)
	else:
		ls = listdir(x)
	try:
		ls.remove("tst.txt")
	except:
		pass
	return ls

if len(sys.argv) >= 2:
	ARG = sys.argv[1]
	if isdir(ARG) and not ARG.endswith("/"):
		ARG += "/"
else:
	raise Exception("Need a playlist path !")



def color(random=True):
	colors = ["32", "31", "34", "2", "3", "33", "35"]
	if random:
		return "\33["+choice(colors)+"m"
	else:
		return ["\33["+x+"m" for x in colors]

def Banner(random=True):
	x = gts()[0]
	x -= len("|____/| .__/ \\___/|_|\\___|_|  |_| |_| |_|\\__,_/_/\\_\\")
	x = x//2
	spaces = " "*x
	ban = """
{} ____            _____                              
{}/ ___| _ __   __|_   _|__ _ __ _ __ ___  _   ___  __
{}\\___ \\| '_ \\ / _ \\| |/ _ \\ '__| '_ ` _ \\| | | \\ \\/ /
{} ___) | |_) | (_) | |  __/ |  | | | | | | |_| |>  < 
{}|____/| .__/ \\___/|_|\\___|_|  |_| |_| |_|\\__,_/_/\\_\\
{}      |_|                                           
""".format(spaces, spaces, spaces, spaces, spaces, spaces)
	if random:
		print(color()+ban+"\33[0m")
	else:
		liste = color(False)
		shuffle(liste)
		for ele in liste:
			sleep(0.1)
			system("clear")
			print(ele+ban+"\33[0m")

def GetMusicVolume():
	system("termux-volume > tst.json")
	volumes = load(open("tst.json"))
	remove("tst.json")
	for volume in volumes:
		if volume["stream"] == "music":
			return (volume["volume"], volume["max_volume"])

def SetMusicVolume(volume):
	system("termux-volume music "+str(volume))

def complete(text, state):
        for cmd in COMMANDS:
                if cmd.startswith(text):
                        if not state:
                                return cmd
                        else:
                                state -= 1

def handleInput():
	global play
	global xit
	global repeat
	global queue
	global liste
	global index
	global COMMANDS
	readline.parse_and_bind("tab: complete")
	readline.set_completer(complete)
	while 1:
		chr = input()
		for chx in chr.split(";"):
			if isfile(ARG+chx):
				play = True
				playSound(ARG+chx)
			elif c(chx) == "pause" and play:
				play = False
				system("termux-media-player pause")
			elif c(chx) == "play" and (not play):
				play = True
				system("termux-media-player play")
			elif c(chx) == "pass" and play:
				playRandom(liste, True)
			elif c(chx) == "clear":
				system("clear")
				Banner()
			elif c(chx) == "back":
				playSound(ARG+last)
			elif c(chx) in ["exit", "quit"]:
				xit = True
				return None
			elif c(chx) in ("list", "ls"):
				print("\n".join(sorted(getSounds())))
			elif chx == "repeat" and (not repeat):
				if len(queue):
					queue.append(last)
					print("Repeating queue !")
				else:
					print(f"Repeating {last} !")
				repeat = True
			elif chx == "unrepeat" and repeat:
				print("Stop repeat !")
				index = 0
				repeat = False
			elif c(chx) == "up":
				v, m_v = GetMusicVolume()
				if v < m_v:
					print("! Mas fuerte ¡")
					SetMusicVolume(v+2)
			elif c(chx) == "down":
				v, m_v = GetMusicVolume()
				if v > 0:
					print("Habla mas bajo")
					SetMusicVolume(v-2)
			elif c(chx) == "banner":
				Banner(False)
			elif c(chx) == "len":
				print(len(liste))
			elif c(chx) == "current":
				print(f"Currently playing {last}")
			elif c(chx) == "infos":
				system("termux-media-player info")
			elif c(chx) == "refresh":
				COMMANDS = ACTIONS[:]
				liste = getSounds()
				for song in liste:
					COMMANDS.append(song)
				print(f"Loaded {len(liste)} songs !")
			elif c(chx) == "queue":
				print("Queue :")
				for e in reversed(queue):
					print(f"\t{e}")
			elif chx.startswith("queue "):
				if chx.split(" ")[1] == "clear":
					print("Clearing queue !")
					queue.clear()
				elif isfile(ARG+" ".join(chx.split(" ")[1:])):
					print(f"{' '.join(chx.split(' ')[1:])} added to queue !")
					queue = [" ".join(chx.split(" ")[1:])] + queue

def checCurrentTrac():
	system("termux-media-player info > tst.txt")
	with open("tst.txt", "r") as r:
		data = r.read()
	remove("tst.txt")
	return (c(data) == "Notrackcurrently!")

def c(data):
	for ele in ["\n"," ","\t","\r"]:
		data = "".join(data.split(ele))
	return data

def playSound(path):
	global last
	system("termux-toast -s -g bottom \"{}\"".format("/".join((".".join(path.replace("_", " ").split(".")[:-1]).split("/")[1:]))))
	system("termux-media-player play \"{}\"".format(path))
	last = path.split("/")[-1]

def playRandom(ls, passing=False):
	global last, index
	if len(queue) != 0 and repeat:
		index = ((index+len(queue))-1)%len(queue)
		playSound(ARG+queue[index])
		return None
	if len(queue) != 0:
		sound = queue.pop()
		playSound(ARG+sound)
		return None
	if repeat and not passing:
		playSound(ARG+last)
		return None
	sound = choice(ls)
	while sound == last:
		sound = choice(ls)
	playSound(ARG+sound)

if len(sys.argv) > 2:
	if c(sys.argv[1]) == "pass":
		playRandom(getSounds())
		sys.exit(0)
	elif c(sys.argv[1]) == "pause":
		system("termux-media-player pause")
		sys.exit(0)
	elif c(sys.argv[1]) == "play":
		system("termux-media-player play")
		sys.exit(0)
	elif c(sys.argv[1]) == "back":
		system("tarmux-toast -s -g bottom \"Couldnt find any ways to do that, sorry <3\"")
		sys.exit(0)

for sound in getSounds():
	COMMANDS.append(sound)
if "--notif" in sys.argv:
	system(f'termux-notification --alert-once -c "SPOTERMUX - Player" --type media --media-next "spotermux {ARG} pass" --media-pause "spotermux {ARG} pause" --media-play "spotermux {ARG} play" --media-previous "spotermux {ARG} back"')

liste = getSounds()
Thread(target=handleInput, daemon=True).start()

system("clear")
Banner()

while 1:
	try:
		if checCurrentTrac() and play:
			playRandom(liste)
		if xit:
			raise KeyboardInterrupt()
	except KeyboardInterrupt:
		print()
		system("termux-media-player stop")
		try:
			remove("tst.txt")
		except:
			pass
		break
	except Exception as e:
		print("An error occured :", e, "!")
sys.exit(0)
