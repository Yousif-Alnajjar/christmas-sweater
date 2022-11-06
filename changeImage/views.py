from django.shortcuts import render
import os
import socket
from threading import Thread
from queue import Queue
import json


class TCPServer(Thread):
    def __init__(self, host, port=65432):
        super().__init__()
        self.host = host
        self.port = port
        self.connected = False
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.host, self.port))
        self.q = Queue(1)

    def run(self):
        while True:
            self.s.listen()
            conn, addr = self.s.accept()
            with conn:
                self.connected = True
                print('hello')
                while True:
                    data = self.q.get()
                    conn.sendall(data)
            self.connected = False

    def isConnected(self): #check if connected before send
        return self.connected

    def send(self, option, topText, bottomText):
        d = {'option': option, 'top': topText, 'bottom': bottomText}
        json_str = json.dumps(d)
        self.q.put(bytes(json_str, 'utf-8'))


# Create your views here.

def home(request):
    count =  0
    dir_path = 'changeImage/static/gifs'
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1
    return render(request, 'home.html', {'imageNumbers': range(1, count)})

def sendData(request):
    count = 0
    dir_path = 'changeImage/static/gifs'
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1
    topText = request.POST['topText']
    bottomText = request.POST['bottomText']
    imageId = request.POST['imageId']
    server = TCPServer("localhost")
    server.start()
    server.send(imageId, topText, bottomText)
    return render(request, 'home.html', {'imageNumbers': range(1, count)})