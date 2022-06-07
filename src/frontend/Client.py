import dotenv
import threading
import socket
import pickle
import time
import pygame
from io import BytesIO
from Player import Player

class Client(threading.Thread):
    def __init__(self, workdir, playerList):
        threading.Thread.__init__(self)
        env = dotenv.dotenv_values('.env')
        if len(env) == 0:
            raise Exception("Env not found")

        self.host = env["HOST"]
        self.port = int(env["PORT"])
        self.playerList = playerList
        self.workdir = workdir
        self.running = False
        self.conn = None
        self._stop_event = threading.Event()

    def open_socket(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.host,self.port))

    def sendRequest(self, request):
        if self.running:
            self.conn.sendall(pickle.dumps(request))
            print('finish send ' + str(pickle.dumps(request)))

    def waitAllPlayers(self, delay=0.1, timeout=10):
        retry = 0
        while len(self.playerList) < 4:
            retry += 1
            time.sleep(0.1)
            if retry * delay >= timeout: break

    def createPlayer(self, id, turn, ours=False):
        self.playerList.insert(turn, Player.Player(pygame.image.load(
            self.work_dir+"/assets/model/model_move.png").convert_alpha(), 3, 320, 320), ours, id)

    def movePlayer(self, turn, movement):
        self.playerList[turn].pressed = True
        self.playerList[turn].moving = True
        if movement == "LEFT":
            self.playerList[turn].animMode = 2
            # self.playerList[turn].move(-32, 0)
            self.playerList[turn].newX = -32
        if movement == "RIGHT":
            self.playerList[turn].animMode = 3
            # self.playerList[turn].move(32, 0)
            self.playerList[turn].newX = 32
        if movement == "UP":
            self.playerList[turn].animMode = 1
            # self.playerList[turn].move(0, -32)
            self.playerList[turn].newY = -32
        if movement == "DOWN":
            self.playerList[turn].animMode = 4
            # self.playerList[turn].move(0, 32)
            self.playerList[turn].newY = 32
        if self.playerList[turn].isOutsideArea():
            self.playerList[turn].newX = 0
            self.playerList[turn].newY = 0
        self.playerList[turn].moving = False
        self.playerList[turn].pressed = False

    """
    Cek jika paket ternyata empty (b'')
    """
    def packetEmpty(self, packet):
        return packet == b''

    def close(self):
        self.running = False
        self.conn.close()
        print('client closed')

    def run(self):
        self.open_socket()
        input = [self.conn]
        self.running = True
        try:

            while self.running:
                packet = self.conn.recv(1024)
                if self.packetEmpty(packet):
                    self.running = False
                    break
                data = BytesIO()
                loaded_data = []
                ptr = 0
                while packet:
                    data.seek(0, 2)
                    data.write(packet)
                    try:
                        while True:
                            data.seek(ptr)
                            loaded_data.append(pickle.load(data))
                            ptr = data.tell()
                    except:
                        """
                        Pickle tidak bisa load, asumsi bahwa
                        paket belum sempurna.
                        Asumsi bahwa loaded_data bisa berisi bisa tidak
                        """
                        for d in loaded_data:
                            print(str(d))
                            if d[0] == "your_id":
                                self.our_player_id = d[2]

                    packet = self.conn.recv(1024)
        except:  self.close()
        finally: self.close()

if __name__ == "__main__":
    playerListTest = []
    c = Client("/", playerListTest)
    c.run()