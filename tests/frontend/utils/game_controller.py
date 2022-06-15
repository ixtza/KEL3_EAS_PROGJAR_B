class GameController:


	def __init__(self, conn):
		self.conn = conn
		self.turn = 0
		# mengubah global var ke atribut entitas
		self.eliminated = []

	"""
	TODO getturn dari server?
	"""
	def getturn(self):
		self.turn = self.conn.getTurn(self.turn) - 1
		return self.turn

	def nextturn(self):
		self.turn = (self.turn + 1) % 4
		while self.turn in self.eliminated and len(self.eliminated) != 4:
			self.turn = (self.turn + 1) % 4

	def getEliminated(self):
		return self.eliminated

	def addEliminated(self, playerid):
		# memperbaiki logic agar memasukan player id yang tidak terdapat pada list eliminsi
		if playerid not in self.eliminated:
			self.eliminated.append(playerid)
			print("NOTICE: Player "+str(playerid)+" gets a break!")

	def addRunOutOfPoints(self, playerid):
		# memperbaiki logic agar memasukan player id yang tidak terdapat pada list eliminsi
		if playerid not in self.eliminated:
			self.eliminated.append(playerid)
			print("NOTICE: Player "+str(playerid)+" has run out of points.")