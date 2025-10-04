import sys
from getkey import getkey, keys
from termcolor import colored

def printOnFile(text, path):
    with open(path, "w") as f:
        f.write(text)

class Player():
    def __init__(self, focus=None, died=False, lives=3):
        self.died = died
        self.focus = focus
        self.writing = ""
        self.lives = lives
        self.menu = False
        self.attackWord = ""

    def getAttackWord(self):
        if self.writing == self.attackWord[:len(self.writing)] and len(self.writing) > 0:
            return colored(self.writing, "red")+colored(self.attackWord[len(self.writing):], "red", attrs=["bold"])
        else:
            return colored(self.attackWord, "red", attrs=['bold'])

    def readMenuKeys(self, key):
        if key == 'j' or key == keys.DOWN:
            self.menu.keyDown()
        elif key == 'k' or key == keys.UP:
            self.menu.keyUp()
        elif ord(key) == 10:
            self.menu.enter()

    def readInputMenu(self, key):
        if ord(key) == 127:
            if len(self.writing) > 0:
                self.writing = self.writing[:-1]
        elif ord(key) == 10:
            self.menu.enter()
        else:
            self.writing += key

    def readInput(self):
        key = getkey()
        if key:
            if self.menu:
                if type(self.menu).__name__ == "MenuController":
                    self.readMenuKeys(key)
                elif type(self.menu).__name__ == "InputMenuController":
                    self.readInputMenu(key)
            else:
                try:
                    key_code = ord(key)
                    if key_code == 127:
                        if len(self.writing) > 0:
                            self.writing = self.writing[:-1]
                    elif key_code == 32:
                        self.shoot()
                    elif key_code == 27:
                        self.quit()
                    elif key_code != 10:
                        self.writing += key
                except Exception as e:
                    print(f"[ERROR] -> {e}", file=sys.stderr)

    def setAttackWord(self, word):
        self.attackWord = word

    def setShooter(self, shootingEvent):
        self.shootingEvent = shootingEvent

    def getWord(self):
        return self.writing

    def shoot(self):
        self.shootingEvent(self.writing)
        self.writing = ""

    def hit(self, damage):
        self.lives -= damage

    def quit(self):
        pass
