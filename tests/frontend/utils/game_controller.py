class GameController:


	def __init__(self, turn):
		self.turn = turn
		# mengubah global var ke atribut entitas
		self.eliminated = []

	"""
	TODO getturn dari server?
	"""
	def getturn(self):
		return self.turn

	def nextturn(self):
		self.turn = (self.turn + 1) % 4
		while self.turn in self.eliminated and len(self.eliminated) is not 4:
			self.turn = (self.turn + 1) % 4

	def getEliminated(self):
		return self.eliminated

	def addEliminated(self, playerid):
		# memperbaiki logic agar memasukan player id yang tidak terdapat pada list eliminsi
		if playerid not in self.eliminated:
			self.eliminated.append(playerid)
			print("Player "+str(playerid)+" gets a break!")

	def addRunOutOfPoints(self, playerid):
		# memperbaiki logic agar memasukan player id yang tidak terdapat pada list eliminsi
		if playerid not in self.eliminated:
			self.eliminated.append(playerid)
			print("Player "+str(playerid)+" has run out of points.")