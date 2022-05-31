import threading
import pickle
from io import BytesIO
from uuid import uuid4

class PlayerConn(threading.Thread):
	def __init__(self, conn, addr, roomManager):
		threading.Thread.__init__(self)
		self.conn = conn
		self.addr = addr
		self.roomManager = roomManager
		self.reqs = []
		self.running = False
		self.id = uuid4()
		self.removed = None

	def sendResponse(self, response):
		if self.running:
			self.conn.sendall(pickle.dump(response))

	def stop(self, removed=False):
		self.removed = removed
		self.running = False
		self._stop_event.set()

	def stopped(self):
		return self._stop_event.is_set()

	def run(self):
		self.running = True
		try:
			while self.running:
				data = bytearray()
				packet = self.conn.recv()
				while packet:
					data.extend(packet)
					packet = self.conn.recv()

				data = bytes(data)
				data = BytesIO(data)
				reqs = []
				try:
					while True:
						reqs.append(pickle.load(data))
				except:
					# Tidak ada lagi request yang masuk
					pass

				for req in reqs:
					pass
					# Command2 masuk di sini
					# Contoh
					# ["play", (gerakan)] -> self.roomManager.playerMove(self.id, gerakan[0], gerakan[1])
		finally:
			if not self.removed and self.roomManager.running:
				self.roomManager.removePlayer(self)

			self.conn.close()
