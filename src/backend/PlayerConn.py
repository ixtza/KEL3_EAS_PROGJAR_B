import threading
import pickle
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

	def sendResponse(self, response):
		if self.running:
			self.conn.sendall(pickle.dumps(response))
			print(self.id + ': finish send ' + str(pickle.dumps(response)))

	def stop(self, removed=False):
		self.removed = removed
		self.running = False
		self.conn.close()
		print(self.id + ' stopped')

	def stopped(self):
		return self.running

	def close(self):
		if not self.removed:
			self.roomManager.removePlayer(self)
		self.conn.close()
		print(self.id + ' closed')

	"""
	Cek jika paket ternyata empty (b'')
	"""
	def packetEmpty(self, packet):
		return packet == b''

	def run(self):
		self.running = True
		self.roomManager.addPlayer(self)

		"""
		Command format selalu
		[cmd_type, sender, data]
		kalau sender = None berarti server kirim
		"""
		self.sendResponse(['your_id', None, self.id])
		try:
			while self.running:
				print(self.id + ' running')
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
							print(self.id + '## reqs')
							print(str(req))
							print(self.id + '## reqs')
							# Command2 masuk di sini
							# Contoh
							# ["play", (gerakan)] -> self.roomManager.playerMove(self.id, gerakan[0], gerakan[1])

					packet = self.conn.recv(1024)
		except:  self.close()
		finally: self.close()
