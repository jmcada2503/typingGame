from getkey import getkey, keys
from playsound import playsound

class Player():
    def __init__(self, focus=None, died=False):
        self.died = died
        self.focus = focus
        self.writing = ""

    def readInput(self):
        key = getkey()
        if key:
            if ord(key) == 127:
                if len(self.writing) > 0:
                    self.writing = self.writing[:-1]
            elif ord(key) == 32:
                self.kill()
            elif ord(key) == 27:
                self.quit()
            elif ord(key) != 10:
                self.writing += key

    def getWord(self):
        return self.writing

    def kill(self):
        self.writing = ""

    def quit(self):
        pass
