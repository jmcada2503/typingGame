from termcolor import colored

class MenuController():
    def __init__(self, player, screenSize, options, decitionEvent, title=None):
        self.screenSize = screenSize
        self.options = options
        self.title = title
        self.selected = 0
        self.decitionEvent = decitionEvent
        self.player = player

    def getMenuSize(self):
        size = len(self.options.keys())
        if self.title:
            size += 2
        return size

    def __str__(self): 
        string = "\n"*((self.screenSize.lines-self.getMenuSize())//2)
        if self.title:
            string += f"{' '*((self.screenSize.columns-len(self.title))//2)}{self.title}\n\n"
        for i in self.options.keys():
            if i == list(self.options.keys())[self.selected]:
                spaces = ' '*(((self.screenSize.columns-len(i))//2)-4)
                string += f"    {colored(spaces+i+spaces, 'white', attrs=['reverse'])}\n"
            else:
                string += f"{' '*((self.screenSize.columns-len(i))//2)}{i}\n"
        string += "\n"*((self.screenSize.lines-self.getMenuSize())//2)
        return string

    def keyDown(self):
        if self.selected < (len(self.options.keys())-1):
            self.selected += 1
        else:
            self.selected = 0 

    def keyUp(self):
        if self.selected > 0:
            self.selected -= 1
        else:
            self.selected = len(self.options.keys())-1

    def enter(self):
        self.player.menu = False
        self.decitionEvent(self.options[list(self.options.keys())[self.selected]])

class InputMenuController():
    def __init__(self, player, screenSize, inputLabel, decitionEvent, title=None):
        self.screenSize = screenSize
        self.inputLabel = inputLabel
        self.title = title
        self.decitionEvent = decitionEvent
        self.player = player

    def getMenuSize(self):
        return 3 if self.title else 1

    def __str__(self): 
        string = "\n"*((self.screenSize.lines-self.getMenuSize())//2)
        if self.title:
            string += f"{' '*((self.screenSize.columns-len(self.title))//2)}{self.title}\n\n"

        maxLength = (self.screenSize.columns-10)-len(self.inputLabel)
        string += f"{' '*4}{self.inputLabel}: "
        if len(self.player.getWord()) > maxLength:
            string += self.player.getWord()[len(self.player.getWord())-maxLength:]+"\n"
        else:
            string += self.player.getWord()+"\n"

        string += "\n"*((self.screenSize.lines-self.getMenuSize())//2)
        return string

    def enter(self):
        self.player.menu = False
        self.decitionEvent(self.player.getWord())
        self.player.writing = ""

