from termcolor import colored
from random import randint

class Enemy():
    def __init__(self, deltaTime, level=1, died=False, speed=1, position=[0,0]):
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

    def getBody(self, writing=""):
        if self.focused:
            return colored(self.word[:len(writing)], 'green')+self.word[len(writing):]
        else:
            return self.word

    def getRandomX(self, ncols):
        return randint(0, (ncols-len(self.word)))

    def step(self):
        if self.movement >= self.speed:
            self.position[1] += 1
            self.movement = 0
        else:
            self.movement += self.deltaTime
