from termcolor import colored
from random import randint

class Enemy():
    def __init__(self, deltaTime, level=1, died=False, speed=1, position=[0,2]):
        self.level = level
        self.died = died
        self.speed = speed
        self.focused = False 

        self.deltaTime = deltaTime
        self.position = position
        self.movement = 0

    def setPosition(self, position):
        self.position = position

    def setWord(self, word):
        self.word = word

    def setFace(self, face):
        self.face = face

    def getBody(self, writing=""):
        body = ""
        if len(self.word) > len(self.face):
            body = [self.word, " "*((len(self.word)-len(self.face))//2)+self.face]
        else:
            body = [" "*((len(self.face)-len(self.word))//2)+self.word, self.face]

        if self.focused:
            body[0] = colored(body[0][:len(writing)], 'green')+body[0][len(writing):]
            body[1] = colored(body[1], "green")

        return body

    def getRandomX(self, ncols):
        return randint(0, (ncols-max([len(i) for i in self.getBody()])))

    def step(self):
        if self.movement >= self.speed:
            self.position[1] += 1
            self.movement = 0
        else:
            self.movement += self.deltaTime
