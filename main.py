import os
import json
import termcolor
import time
from threading import Thread
from random import randint

from classes.player import Player
from classes.enemy import Enemy
from classes.menuController import *
from classes.onlineController import *

def printOnFile(text, path):
    with open(path, "w") as f:
        f.write(text)

def getRandomWord(words):
    return words[randint(0, len(words)-1)]

def readJson(path):
    with open(path, "r") as f:
        return json.load(f)


class EnemyController():

    def __init__(self, deltaTime, spawnSpeed=1):
        self.enemiesSpeed = 0.5
        self.enemies = []
        self.deltaTime = deltaTime
        self.spawnSpeed = spawnSpeed
        self.spawning = 0
        self.waitingList = []

    def setFocusedEnemies(self, word):
        for i in self.enemies:
            if word == i.word[:len(word)] and len(word) > 0:
                i.focused = True
            else:
                i.focused = False

    def newEnemy(self, words, screenSize):
        enemy = Enemy(self.deltaTime, level=1, died=False, speed=self.enemiesSpeed)
        enemy.setWord(getRandomWord(words[str(enemy.level)]))
        enemy.setPosition([enemy.getRandomX(screenSize.columns), 0])
        self.enemies.append(enemy)
        return enemy

    def newDefinedEnemy(self, word, screenSize):
        enemy = Enemy(self.deltaTime, level=1, died=False, speed=self.enemiesSpeed)
        enemy.setWord(word)
        enemy.setPosition([enemy.getRandomX(screenSize.columns), 1])
        self.enemies.append(enemy)
        return enemy

    def addToWaitingList(self, words: list):
        self.waitingList += words

    def getEnemies(self):
        return self.enemies

    def playerShootEvent(self, word):
        for i in self.enemies:
            if i.word == word:
                i.died = True

    def enemySpawner(self, words, screenSize):
        if self.spawning >= self.spawnSpeed:
            self.newEnemy(words, screenSize)
            self.spawning = 0
        else:
            self.spawning += self.deltaTime

    def enemyOnlineSpawner(self, screenSize):
        if self.spawning >= self.spawnSpeed:
            if len(self.waitingList) > 0:
                self.newDefinedEnemy(self.waitingList[0], screenSize)
                self.waitingList = self.waitingList[1:]
            self.spawning = 0
        else:
            self.spawning += self.deltaTime

    def enemyAttack(self, screenSize):
        damage = 0
        newEnemies = []
        for i in range(len(self.enemies)):
            if (self.enemies[i].position[1] > (screenSize.lines-3)):
                if self.enemies[i].died == False:
                    damage += 1
            else:
                newEnemies.append(self.enemies[i])
        self.enemies = newEnemies

        return damage

class game():

    def __init__(self, player):
        self.deltaTime = 0.1
        self.screenSize = os.get_terminal_size()
        self.player = player
        self.inGame = True
        self.inputThread = Thread(target=self.readPlayerInput)
        self.inputThread.start()

    def quitGame(self):
        self.inGame = False
        os.system("clear")
        exitMenu = MenuController(player=self.player, screenSize=self.screenSize, options={}, decitionEvent=self.menuSelect, title="Press any button to exit ...")
        print(exitMenu)
        exit()

    def readPlayerInput(self):
        while self.inGame:
            player.readInput()

    def menuSelect(self, selection):
        self.openMenu = False
        self.menuSelection = selection

    def startMenu(self):
        self.openMenu = True
        onlineMenu = MenuController(player=self.player, screenSize=self.screenSize, options={
            "Single Player": 0,
            "Multi Player": 1
            }, decitionEvent=self.menuSelect, title="MAIN MENU")
        self.player.menu = onlineMenu

        while self.openMenu:
            start = time.time()
            menuStr = str(onlineMenu)
            os.system("clear")
            print(menuStr)
            end = time.time()
            time.sleep(mainGame.deltaTime - (end-start))

        if self.menuSelection == 0:
            self.singlePlayer()
        elif self.menuSelection == 1:
            self.multiPlayer()

    def buildLine(self, line):
        enemiesLine = []
        for i in self.enemyController.getEnemies():
            if i.position[1] == line and i.died == False:
                enemiesLine.append(i)

        if len(enemiesLine)>0:
            return " "*enemiesLine[0].position[0]+enemiesLine[0].getBody(self.player.getWord())
        else:
            return ""


    def singlePlayer(self):
        self.words = readJson("./data/words.json")
        self.enemyController = EnemyController(self.deltaTime, spawnSpeed=0.5)
        self.enemyController.newEnemy(self.words, self.screenSize) 
        self.player.setShooter(self.enemyController.playerShootEvent)
        self.player.lives = 3
        self.player.menu = False
        self.player.writing = ""

        self.mainLoop()

    def multiPlayer(self):
        self.openMenu = True
        multiPlayerStartMenu = MenuController(player=self.player, screenSize=self.screenSize, options={
            "Connect to Server": 0,
            "Create Server": 1
            }, decitionEvent=self.menuSelect, title="MULTI PLAYER")
        self.player.menu = multiPlayerStartMenu

        while self.openMenu:
            start = time.time()
            menuStr = str(multiPlayerStartMenu)
            os.system("clear")
            print(menuStr)
            end = time.time()
            time.sleep(mainGame.deltaTime - (end-start))

        if self.menuSelection == 0:
            # Connect to a server
            self.openMenu = True
            ipAddressMenu = InputMenuController(player=self.player, screenSize=self.screenSize, inputLabel="Server ip", decitionEvent=self.menuSelect, title="CONNECT TO SERVER")
            self.player.menu = ipAddressMenu
            while self.openMenu:
                start = time.time()
                menuStr = str(ipAddressMenu)
                os.system("clear")
                print(menuStr)
                end = time.time()
                time.sleep(mainGame.deltaTime - (end-start))

            self.client = ClientController(self.deltaTime)
            self.client.startClient(self.menuSelection)

            self.clientPlayerGame()

        elif self.menuSelection == 1:
            # Create server

            # Start server with given name
            self.server = ServerController(self.deltaTime)
            self.server.startServer()

            # Wait for other player
            waitForPlayer = MenuController(player=self.player, screenSize=self.screenSize, options={f"Server ip: {self.server.ip}":0}, decitionEvent=self.menuSelect, title="Waiting for the other player ...")
            self.player.menu = waitForPlayer
            while not(self.server.clientPlayerUp()):
                start = time.time()
                menuStr = str(waitForPlayer)
                self.server.readServerInfo()
                os.system("clear")
                print(menuStr)
                end = time.time()
                time.sleep(mainGame.deltaTime - (end-start))

            self.serverPlayerGame()

    def serverShootEvent(self, word):
        self.enemyController.playerShootEvent(word)
        if self.player.attackWord != "":
            if self.player.attackWord == word:
                self.server.serverAttack(word)
                self.player.setAttackWord(getRandomWord(self.words[str(randint(1, 3))]))

    def clientShootEvent(self, word):
        self.enemyController.playerShootEvent(word)
        if self.player.attackWord != "":
            if self.player.attackWord == word:
                self.client.clientAttack(word)
                self.player.setAttackWord(getRandomWord(self.words[str(randint(1, 3))]))

    def serverPlayerGame(self):
        self.words = readJson("./data/words.json")
        self.enemyController = EnemyController(self.deltaTime, spawnSpeed=0.5)
        self.server.connectionSpeed = self.enemyController.spawnSpeed
        self.player.setShooter(self.serverShootEvent)
        self.player.setAttackWord(getRandomWord(self.words[str(randint(1, 3))]))
        self.player.lives = 3
        self.player.menu = False
        self.player.writing = ""
        clock = 0

        while True:
            start = time.time()

            # Game code
            
            self.enemyController.setFocusedEnemies(self.player.getWord())

            # Enemy Attack
            self.player.hit(self.enemyController.enemyAttack(self.screenSize))
            if self.player.lives <= 0:
                break

            # Check for new words on server
            self.server.readServerInfo()
            self.enemyController.addToWaitingList(self.server.getServerNewWords())

            # Call Enemy spawner
            self.enemyController.enemyOnlineSpawner(self.screenSize)
            
            for enemy in self.enemyController.getEnemies():
                # Move the enemy
                enemy.step()

            os.system("clear")
            for line in range(self.screenSize.lines-2):
                print(self.buildLine(line))
            print(f"{' '*((self.screenSize.columns-3)//2)}/^\\\n  lives: {player.lives}{' '*(((self.screenSize.columns-5)//2)-(9+len(str(player.lives))))}/~~~\\{' '*(((self.screenSize.columns-5)//2)-(2+len(self.player.attackWord)))}{self.player.getAttackWord()}\n"+f"{' '*((self.screenSize.columns-len(self.player.getWord()))//2)}{self.player.getWord()}", end="")

            end = time.time()
            time.sleep(self.deltaTime - (end-start))
            clock += self.deltaTime

        self.openMenu = True
        endGameMenu = MenuController(player=self.player, screenSize=self.screenSize, options={
            "Restart": 0,
            "Exit": 1
            }, decitionEvent=self.menuSelect, title="GAME OVER")
        self.player.menu = endGameMenu

        while self.openMenu:
            start = time.time()
            menuStr = str(endGameMenu)
            os.system("clear")
            print(menuStr)
            end = time.time()
            time.sleep(mainGame.deltaTime - (end-start))

        if self.menuSelection == 0:
            self.startMenu()
        elif self.menuSelection == 1:
            self.quitGame()

    def clientPlayerGame(self):
        self.words = readJson("./data/words.json")
        self.enemyController = EnemyController(self.deltaTime, spawnSpeed=0.5)
        self.client.connectionSpeed = self.enemyController.spawnSpeed
        self.player.setShooter(self.clientShootEvent)
        self.player.setAttackWord(getRandomWord(self.words[str(randint(1, 3))]))
        self.player.lives = 3
        self.player.menu = False
        self.player.writing = ""
        clock = 0

        while True:
            start = time.time()

            # Game code
            
            self.enemyController.setFocusedEnemies(self.player.getWord())

            # Enemy Attack
            self.player.hit(self.enemyController.enemyAttack(self.screenSize))
            if self.player.lives <= 0:
                break

            # Check for new words on server
            self.enemyController.addToWaitingList(self.client.getClientNewWords())

            # Call Enemy spawner
            self.enemyController.enemyOnlineSpawner(self.screenSize)
            
            for enemy in self.enemyController.getEnemies():
                # Move the enemy
                enemy.step()

            os.system("clear")
            for line in range(self.screenSize.lines-2):
                print(self.buildLine(line))
            print(f"{' '*((self.screenSize.columns-3)//2)}/^\\\n  lives: {player.lives}{' '*(((self.screenSize.columns-5)//2)-(9+len(str(player.lives))))}/~~~\\{' '*(((self.screenSize.columns-5)//2)-(2+len(self.player.attackWord)))}{self.player.getAttackWord()}\n"+f"{' '*((self.screenSize.columns-len(self.player.getWord()))//2)}{self.player.getWord()}", end="")

            end = time.time()
            time.sleep(self.deltaTime - (end-start))
            clock += self.deltaTime

        self.openMenu = True
        endGameMenu = MenuController(player=self.player, screenSize=self.screenSize, options={
            "Restart": 0,
            "Exit": 1
            }, decitionEvent=self.menuSelect, title="GAME OVER")
        self.player.menu = endGameMenu

        while self.openMenu:
            start = time.time()
            menuStr = str(endGameMenu)
            os.system("clear")
            print(menuStr)
            end = time.time()
            time.sleep(mainGame.deltaTime - (end-start))

        if self.menuSelection == 0:
            self.startMenu()
        elif self.menuSelection == 1:
            self.quitGame()

    def mainLoop(self):
        clock = 0

        while True:
            start = time.time()

            # Game code
            
            self.enemyController.setFocusedEnemies(self.player.getWord())

            # Enemy Attack
            self.player.hit(self.enemyController.enemyAttack(self.screenSize))
            if self.player.lives <= 0:
                break

            # Call Enemy spawner
            self.enemyController.enemySpawner(self.words, self.screenSize)
            
            for enemy in self.enemyController.getEnemies():
                # Move the enemy
                enemy.step()

            os.system("clear")
            for line in range(self.screenSize.lines-2):
                print(self.buildLine(line))
            print(f"{' '*((self.screenSize.columns-3)//2)}/^\\\n  lives: {player.lives}{' '*(((self.screenSize.columns-5)//2)-(9+len(str(player.lives))))}/~~~\\\n"+f"{' '*((self.screenSize.columns-len(self.player.getWord()))//2)}{self.player.getWord()}", end="")

            end = time.time()
            time.sleep(self.deltaTime - (end-start))
            clock += self.deltaTime

        self.openMenu = True
        endGameMenu = MenuController(player=self.player, screenSize=self.screenSize, options={
            "Restart": 0,
            "Exit": 1
            }, decitionEvent=self.menuSelect, title="GAME OVER")
        self.player.menu = endGameMenu

        while self.openMenu:
            start = time.time()
            menuStr = str(endGameMenu)
            os.system("clear")
            print(menuStr)
            end = time.time()
            time.sleep(mainGame.deltaTime - (end-start))

        if self.menuSelection == 0:
            self.startMenu()
        elif self.menuSelection == 1:
            self.quitGame()


if __name__ == "__main__":
    player = Player()
    
    mainGame = game(player)

    mainGame.startMenu()
