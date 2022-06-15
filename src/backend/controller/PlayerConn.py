import threading
import pickle
import socket
import time
from io import BytesIO
from uuid import uuid4

class PlayerConn(threading.Thread):
	def __init__(self, conn, addr, manager, roomManager):
		threading.Thread.__init__(self)
		self.conn = conn
		self.addr = addr
		self.manager = manager
		self.roomManager = roomManager
		self.reqs = []
		self.running = False
		self.id = str(uuid4())
		self.removed = None
		self.turn = None

	def sendResponse(self, response):
		def send():
			try:
				self.conn.sendall(pickle.dumps(response))
				# print(self.id + ': finish send ' + str(response))
			except BrokenPipeError as e:
				# print(self.id + ': finish send with brokenpipe ' + str(response))
				pass

		if self.running:
			threading.Thread(target=send).start()

	def stop(self, removed=False):
		self.removed = removed
		self.running = False

		try: 	 self.conn.shutdown(socket.SHUT_RDWR)
		except:  pass
		finally: self.conn.close()

		print(self.id + ' stopped')

	def stopped(self):
		return self.running

	def close(self):
		if not self.removed:
			self.roomManager.removePlayer(self)

		try: 	 self.conn.shutdown(socket.SHUT_RDWR)
		except:  pass
		finally: self.conn.close()

		# print(self.id + ' closed')

	"""
	Cek jika paket ternyata empty (b'')
	"""
	def packetEmpty(self, packet):
		return packet == b''

	def routeHandler(self, req):
		if req[0] == "broadcast_arena_config":
			print("RECV BROADCAST ARENA CONFIG")
			req[2]["id"] = self.id
			self.roomManager.addArenaConfig(self, req[2])
			self.sendResponse(['broadcast_arena_config_done', None, None])
		elif req[0] == "player_ready":
			self.roomManager.playerReady(self, req[2])
			self.roomManager.sendAllPlayerReady(self)
		elif req[0] == "get_turn":
			self.roomManager.sendTurn(self)
		elif req[0] == "broadcast_player_action":
			self.roomManager.broadcastAction(self, req[2])
		elif req[0] == "ask_all_player_ready":
			self.roomManager.askAllReady(self)
		elif req[0] == "ask_arena_config":
			self.roomManager.sendArenaConfig(self)
		elif req[0] == "sync_player_state":
			print("receive sync from " + str(self.id) + ": " + str(req[2]))
			self.roomManager.syncPlayerState(self, req[2])

	def run(self):
		self.running = True
		self.sendResponse(['your_id', None, self.id])
		self.roomManager.addPlayer(self)

		"""
		Command format selalu
		[cmd_type, sender, data]
		kalau sender = None berarti server kirim
		"""
		print(self.id + ' running')
		try:
			while self.running:
				packet = self.conn.recv(1024)
				if self.packetEmpty(packet):
					self.running = False
					break
				data = BytesIO()
				reqs = []
				ptr = 0
				while packet:
					data.seek(0, 2)
					data.write(packet)
					try:
						while True:
							data.seek(ptr)
							reqs.append(pickle.load(data))
							ptr = data.tell()
					except:
						"""
						Pickle tidak bisa load, asumsi bahwa
						paket belum sempurna.
						Asumsi bahwa reqs bisa berisi bisa tidak
						"""
						for req in reqs:
							# print(self.id + str(req))
							# Command2 masuk di sini
							# Contoh: ["play", (gerakan)] -> self.roomManager.playerMove(self.id, gerakan[0], gerakan[1])
							self.routeHandler(req)
							reqs.remove(req)

					packet = self.conn.recv(1024)
		except ConnectionResetError as e:  pass
		# except: pass
		finally: self.close()
