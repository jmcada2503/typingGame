import os
import json
import termcolor
import time
from threading import Thread
from random import randint

from classes.player import Player
from classes.enemy import Enemy

def printOnFile(text, path):
    with open(path, "w") as f:
        f.write(text)

def getRandomWord(words):
    return words[randint(0, len(words)-1)]

def readJson(path):
    with open(path, "r") as f:
        return json.load(f)

def readPlayerInput(player):
    while True:
        player.readInput()

class game():

    def __init__(self):
        self.deltaTime = 0.05
        self.nEnemies = 5

    def buildLine(self, line):
        lineStr = " "*self.screenSize.columns
        enemiesLine = []
        for i in self.enemies:
            if i.position[1] == line:
                enemiesLine.append(i)

        problems = [[[-1, -1], []]]
        for i in range(len(enemiesLine)):
            noProblem = True
            for problem in range(len(problems)):
                if (enemiesLine[i].position[0] >= problems[problem][0][0] and enemiesLine[i].position[0] <= problems[problem][0][1]) or (enemiesLine[i].position[0]+(len(enemiesLine[i].getBody())-1) <= problems[problem][0][1] and enemiesLine[i].position[0]+(len(enemiesLine[i].getBody())-1) >= problems[problem][0][0]):
                    noProblem = False
                    problems[problem][0][0] = min(problems[problem][0][0], enemiesLine[i].position[0])
                    problems[problem][0][1] = max(problems[problem][0][1], enemiesLine[i].position[0]+(len(enemiesLine[i].getBody())-1))
                    problems[problem][1].append(enemiesLine[i])
                    break
            if noProblem:
                problems.append([[enemiesLine[i].position[0], enemiesLine[i].position[0]+(len(enemiesLine[i].getBody())-1)], [enemiesLine[i]]])
        problems = problems[1:]

        for i in range(len(problems)):
            for j in range(len(problems[i][1])-1):
                for k in range(len(problems[i][1])-1):
                    if problems[i][1][k].focused and problems[i][1][k+1].focused == False:
                        problems[i][1][k], problems[i][1][k+1] = problems[i][1][k+1], problems[i][1][k]

        for i in range(len(problems)):
            for j in range(len(problems[i][1])):
                lineStr = lineStr[:problems[i][1][j].position[0]+1] + problems[i][1][j].getBody(self.player.getWord())

        return lineStr

        
    def setFocusedEnemies(self):
        for i in self.enemies:
            if self.player.getWord() == i.word[:len(self.player.getWord())] and len(self.player.getWord()) > 0:
                i.focused = True
            else:
                i.focused = False

    def main(self, player):
        self.screenSize = os.get_terminal_size()

        self.player = player
        self.words = readJson("./data/words.json")
        self.enemies = []
        for i in range(self.nEnemies):
            self.enemies.append(Enemy(self.deltaTime, level=1, died=False, speed=0.5))
        line = 0
        for enemy in range(len(self.enemies)):
            self.enemies[enemy].setWord(getRandomWord(self.words[str(self.enemies[enemy].level)]))
            self.enemies[enemy].setPosition([self.enemies[enemy].getRandomX(self.screenSize.columns), line])
            line -= 2

        self.mainLoop()


    def mainLoop(self):
        clock = 0

        while True:
            start = time.time()

            os.system("clear")
            # Game code

            self.setFocusedEnemies()

            for enemy in self.enemies:
                # Move the enemy
                enemy.step()

            for line in range(self.screenSize.lines-2):
                flag = True
                print(self.buildLine(line))
            print(f"{' '*((self.screenSize.columns-3)//2)}/^\\\n{' '*((self.screenSize.columns-5)//2)}/~~~\\\n"+f"{' '*((self.screenSize.columns-len(self.player.getWord()))//2)}{self.player.getWord()}", end="")

            end = time.time()
            time.sleep(self.deltaTime - (end-start))
            clock += self.deltaTime


if __name__ == "__main__":
    player = Player()
    t = Thread(target=readPlayerInput, args=[player])
    t.start()
    mainGame = game()
    mainGame.main(player)
