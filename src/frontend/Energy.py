class Energy:
	def __init__(self, img, x, y):
		self.img = img
		self.x = x
		self.y = y

	def print(self, screen):
		screen.blit(self.img, (self.x, self.y))

	def getX(self):
		return self.x

	def getY(self):
		return self.y
