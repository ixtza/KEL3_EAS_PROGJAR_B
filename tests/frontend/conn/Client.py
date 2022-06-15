import dotenv
import threading
import socket
import pickle
import time
import pygame
from io import BytesIO

class Client(threading.Thread):
    def __init__(self, game):
        threading.Thread.__init__(self)
        env = dotenv.dotenv_values('.env')
        if len(env) == 0:
            raise Exception("Env not found")

        self.host = env["HOST"]
        self.port = int(env["PORT"])
        self.running = False
        self.conn = None
        self._stop_event = threading.Event()
        self.game = game
        self.connected_players = {}
        self.arena_config = None
        self.all_player_ready = None
        self.current_player_turn_buff = None
        self.current_player_turn = None

    def open_socket(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.host,self.port))
        print("CONNECT: " + str(self.conn.getsockname()))

    def sendRequest(self, request):
        def send():
            self.conn.sendall(pickle.dumps(request))
            print('finish send ' + str(request))

        if self.running:
            threading.Thread(target=send).start()

    def getArenaConfig(self):
        while not self.arena_config:
            time.sleep(0.1)

        return self.arena_config
        arena_configuration = {
				"id": None,
				"illegal_place": [(5, 5)],
				"players": [],
				"loss": [],
				"breaks": [],
				"energys": [],
				"num_of_breaks": 12,
				"num_of_energys": 12,
				"num_of_loss": 12,
			}

    def getAllPlayersIdTurn(self):
        if not self.waitAllPlayers(): return
        return self.connected_players

    def waitAllPlayers(self, delay=0.1, timeout=30):
        retry = 0
        while len(self.connected_players) < 4:
            retry += 1
            time.sleep(0.1)
            if retry * delay >= timeout:
                return False
        return True

    def waitAllPlayerReady(self):
        self.sendRequest(["player_ready", self.our_player_id, None])
        retry = 0
        timeout = 10
        while not self.all_player_ready:
            retry += 1
            time.sleep(0.1 * retry)
            if 0.1 * retry >= timeout: break

        while not self.all_player_ready:
            # self.sendRequest(["ask_all_player_ready", self.our_player_id, None])
            self.sendRequest(["player_ready", self.our_player_id, None])
            time.sleep(3)

        self.all_player_ready = False
        return

    def sendReady(self):
        self.sendRequest(["player_ready", self.our_player_id, None])

    def sendAction(self, action):
        self.sendRequest(["broadcast_player_action", None, action])

    """
    Cek jika kita adalah player 1
    """
    def isRoomHost(self):
        return self.our_player_turn == 1

    def broadcastArenaConfig(self, arena_config):
        self.sendRequest(["broadcast_arena_config", None, arena_config])
        pass

    def getTurn(self, current_turn):
        self.sendRequest(["get_turn", None, None])
        while not self.current_player_turn_buff:
            time.sleep(0.1)

        if self.current_player_turn_buff == 0:
            self.current_player_turn_buff = None
            return self.getTurn()

        # if self.current_player_turn_buff == current_turn:
        #     return self.getTurn()

        self.current_player_turn = self.current_player_turn_buff
        self.current_player_turn_buff = None
        return self.current_player_turn

    """
    Cek jika paket ternyata empty (b'')
    """
    def packetEmpty(self, packet):
        return packet == b''

    def close(self):
        self.running = False
        self.conn.shutdown(socket.SHUT_RDWR)
        self.conn.close()
        print('client closed')

    def responseHandler(self, resp):
        print(str(resp))
        if resp[0] == "your_id":
            self.our_player_id = resp[2]
            self.connected_players[self.our_player_id] = {}
        elif resp[0] == "your_turn":
            self.our_player_turn = resp[2]
            self.connected_players[self.our_player_id]["turn"] = resp[2]
        elif resp[0] == "player_enter":
            self.connected_players[resp[2][0]] = {
                "turn": resp[2][1]
            }
        elif resp[0] == "broadcast_arena_config":
            self.arena_config = resp[2]
        elif resp[0] == "all_player_ready":
            self.all_player_ready = True
        elif resp[0] == "player_turn":
            self.current_player_turn_buff = resp[2]
        elif resp[0] == "player_action":
            keydown_action = {
                "keydown": True,
                "left": False,
                "right": False,
                "up": False,
                "down": False,
                "keyup": False,
            }
            # keyup_action = {
            #     "keydown": False,
            #     "keyup": True,
            # }
            keydown_action[resp[2]] = True
            # obj = self.connected_players[resp[1]]["object"]
            # threading.Thread(target=obj.check_movement, args=(keydown_action, True))
            self.connected_players[resp[1]]["object"].check_movement(keydown_action, True)
        elif resp[0] == "player_need_ready":
            pass
        elif resp[0] == "end_game":
            if resp[2][0] == "player_leave":
                self.game.force_exit()

    def run(self):
        self.open_socket()
        self.running = True

        try:
            while self.running:
                packet = self.conn.recv(1024)
                # if self.packetEmpty(packet):
                #     self.running = False
                #     break
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
                            self.responseHandler(d)
                            loaded_data.remove(d)

                    packet = self.conn.recv(1024)
        # except:  self.close()
        finally: self.game.force_exit()
