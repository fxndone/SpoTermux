from .commands import *
from .utils import *
from .config import *
import time
import threading


def find_player():
    if exec_command("termux-media-player help")[1] == 0:
        return 0
    elif exec_command("mpg123 -?")[1] == 0:
        return 1
    elif exec_command("ffplay -h")[1] == 0:
        return 2
    # elif exec_command("afplay -h")[1] == 0:
    #     return 2
    else:
        try:
            import playsound
        except:
            return
        return 3

class Player:
    def __init__(self):
        player = find_player()
        self.is_playing = None
        self.last = None
        if player is None:
            raise Exception("Could not find any music player !\nPlease see README file !")
        if player == 0:
            self.run = self.__termux_media_player_play
            self.check_play = self.__termux_media_player_info
        elif player == 1:
            self.run = self.__mpg123
            self.check_play = self.__default_check_play
        elif player == 2:
            self.run = self.__ffplay
            self.check_play = self.__default_check_play
        elif player == 3:
            self.run = self.__playsound
            self.check_play = self.__default_check_play
    
    def __default_check_play(self):
        return self.is_playing
    
    def __mpg123(self, filename):
        threading.Thread(target=self.__mpg123_play, args=(filename,), daemon=True).start()
    
    def __mpg123_play(self, filename):
        self.is_playing = True
        self.last = filename
        exec_command("mpg123 -q " + filename)
        self.is_playing = False

    def __termux_media_player_play(self, filepath):
        self.last = filepath
        exec_command("termux-media-player play " + filepath)

    def __termux_media_player_info(self):
        return exec_command("termux-media-player info")[0] != cleared_string("Notrackcurrently!")
    
    def __playsound(self, filename):
        threading.Thread(target=self.__playsound_play, args=(filename,), daemon=True).start()

    def __playsound_play(self, filename):
        self.last = filename
        __import__('playsound').playsound(filename)
        self.is_playing = True
        time.sleep(self.get_music_duration(filename))
        self.is_playing = False
    
    def __ffplay(self, filename):
        threading.Thread(target=self.__ffplay_play, args=(filename,), daemon=True).start()
    
    def __ffplay_play(self, filename):
        self.is_playing = True
        self.last = filename
        exec_command(f"ffplay -vn -nodisp {filename}")
        self.is_playing = False
    
    def get_music_duration(self, filename):
        if exec_command("ffmpeg -h")[1] == 0:
            out = exec_command("ffmpeg -i " + filename + " 2>&1 |grep -oP \"[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{2}\"")[0]
            if out.count(":") != 2:
                return None
            h, m, s = cleared_string(out).split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)
        if exec_command("ffprob -h")[1] == 0:
            return float(exec_command(f"ffprobe -show_entries stream=duration -of compact=p=0:nk=1 -v fatal {filename}"))