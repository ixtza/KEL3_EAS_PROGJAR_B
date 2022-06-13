import select
import socket
import sys
import threading
import math
import dotenv
from exception.ServerEnvException import ServerEnvException
from manager.ConnManager import ConnManager
from manager.RoomManager import RoomManager

class Server:
	def __init__(self, manager, clientManager):
		env = dotenv.dotenv_values('.env')
		if len(env) == 0:
			raise ServerEnvException("Env not found")

		self.host = env["HOST"]
		self.port = int(env["PORT"])
		self.backlog = int(env["BACKLOG"])
		self.silent = bool(env["SILENT"])
		self.manager = manager
		self.clientManager = clientManager
		self.running = False

	def open_socket(self):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server.bind((self.host,self.port))
		self.server.listen(self.backlog) # karena docs -> https://docs.python.org/3/library/socket.html

	def print(self, str):
		if not self.silent: print(str)

	def run(self):
		self.open_socket()
		input = [self.server]
		self.running = True
		manager = self.manager(self.clientManager)
		while self.running:
			inputready, outputready, exceptready = select.select(input,[],[])

			for s in inputready:
				if s == self.server:
					# handle the server socket
					client_socket, client_address = self.server.accept() # revise
					manager.push(client_socket,client_address)
					# self.threads.append(c)
				elif s == sys.stdin:
					# handle standard input
					junk = sys.stdin.readline()
					manager.stop()
					self.running = False


	 # close all threads
		# self.server.close()
		# for c in self.threads:
		# 	c.join()

if __name__ == "__main__":
	s = Server(ConnManager, RoomManager)
	s.run()
