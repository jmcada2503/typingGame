from flask import Flask, jsonify, request
from threading import Thread
import requests
import json
import socket
import logging

server = Flask(__name__)
serverPort = 4000

log = logging.getLogger('werkzeug')
log.disabled = True

def readData():
    f = open(f"./data/server/data{serverPort}.json", "r")
    data = json.load(f)
    f.close()
    return data

def writeData(data):
    f = open(f"./data/server/data{serverPort}.json", "w")
    f.write(json.dumps(data))
    f.close()

@server.route('/status', methods=["GET"])
def serverStatus():
    return jsonify({"status":"up"})

@server.route('/setClientPlayer', methods=["GET"])
def setClientPlayerUp():
    data = readData()
    data["clientPlayer"] = "up"
    writeData(data)
    return jsonify({"clientPlayer":"up", "serverPlayer":"up"})

@server.route('/clientAttack', methods=["GET"])
def clientAttack():
    data = readData()
    data["serverNewWords"].append(request.args.get("word"))
    writeData(data)
    return jsonify({"newWord":"ok"})

@server.route("/clientNewWords", methods=["GET"])
def clientNewWords():
    data = readData()
    words = data["clientNewWords"]
    data["clientNewWords"] = []
    writeData(data)
    return jsonify({"clientNewWords":words, "status": "up"})

class ServerController():

    def __init__(self, deltaTime, connectionSpeed=0.5):
        global server
        self.server = server
        self.data = {"serverNewWords":[], "clientNewWords":[]}
        self.deltaTime = deltaTime
        self.connectionSpeed = connectionSpeed
        self.connecting = 0

    def writeServerInfo(self):
        f = open(f"./data/server/data{self.port}.json", "w")
        f.write(json.dumps(self.data))
        f.close()

    def readServerInfo(self):
        f = open(f"./data/server/data{self.port}.json", "r")
        self.data = json.load(f)
        f.close()

    def getServerNewWords(self):
        words = self.data["serverNewWords"]
        self.data["serverNewWords"] = []
        self.writeServerInfo()
        return words

    def startServer(self):
        global serverPort

        self.data["serverPlayer"] = "up"

        port = 4000
        for i in range(4000, 5001):
            try:
                response = requests.get(f"http://localhost:{i}/status")
            except:
                port = i
                break

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.ip = s.getsockname()[0]

        self.port = port
        serverPort = port

        self.serverThread = Thread(target=self.server.run, kwargs={"port":port, "host":"0.0.0.0"})
        self.serverThread.start()

        self.writeServerInfo()

    def clientPlayerUp(self):
        try:
            return self.data["clientPlayer"] == "up"
        except:
            return False

    def serverAttack(self, word):
        self.data["clientNewWords"].append(word)
        self.writeServerInfo()


class ClientController():
    def __init__(self, deltaTime, connectionSpeed=0.5):
        self.port = 4000
        self.deltaTime = deltaTime
        self.connectionSpeed = connectionSpeed
        self.connecting = 0

    def startClient(self, ip):
        self.ip = ip

        for i in range(4000, 5000):
            response = requests.get(f"http://{self.ip}:{i}/status")
            if response.json()["status"] == "up":
                self.port = i
                break

        requests.get(f"http://{self.ip}:{self.port}/setClientPlayer")

    def clientAttack(self, word):
        response = requests.get(f"http://{self.ip}:{self.port}/clientAttack", params={"word":word})

    def getClientNewWords(self):
        if self.connecting >= self.connectionSpeed:
            response = requests.get(f"http://{self.ip}:{self.port}/clientNewWords")
            data = response.json()
            words = data.get("clientNewWords")
            self.connecting = 0
            return words
        else:
            self.connecting += self.deltaTime
            return []
