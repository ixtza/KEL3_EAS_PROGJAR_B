import pygame

class Energy:
	def __init__(self, img, x, y):
		self.img = img
		self.x = x
		self.y = y

		# collision
		self.rect = pygame.Rect(x, y, 32, 32)

		# is picked
		self.is_picked = False

	def getX(self):
		return self.x

	def getY(self):
		return self.y

	def get_hits(self, players):
		hits = []
		for player in players:
			if player.is_alive  == True:
				if self.rect.colliderect(player.rect):
					self.is_picked = True
					hits.append(player)
		return hits
	
	def check_collision(self, players):
		if self.is_picked == False:
			entities = self.get_hits(players)
			for entity in entities:
				entity.point += 3

	def update(self, players):
		self.check_collision(players)
		pass
		
	def render(self, display):
		if self.is_picked != True:
			display.blit(self.img, (self.x, self.y))
