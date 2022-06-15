import threading
import pickle
from io import BytesIO
from ..controller.PlayerConn import PlayerConn
from RoomManager import RoomManager

class ConnManager():
	def __init__(self, clientManager, silent=False):
		self.silent = silent
		self.clients = []
		self.clientManager = clientManager()

	def push(self, conn, addr):
		player = PlayerConn(conn, addr, self, self.clientManager)
		self.clients.append(player)
		player.start()

	def print(self, str):
		if not self.silent: print(str)

	def stop(self):
		self.clientManager.stop()
		for client in self.clients:
			client.stop()