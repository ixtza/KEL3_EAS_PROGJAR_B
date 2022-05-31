class GameController:

	eliminated = []

	def __init__(self, turn):
		self.turn = turn

	def getturn(self):
		return self.turn

	def nextturn(self):
		self.turn = (self.turn + 1) % 4
		while self.turn in self.eliminated:
			self.turn = (self.turn + 1) % 4

	def getEliminated(self):
		return self.eliminated

	def addEliminated(self, playerid):
		self.eliminated.append(playerid)
		print("Player"+str(playerid+1)+" gets a break!")
