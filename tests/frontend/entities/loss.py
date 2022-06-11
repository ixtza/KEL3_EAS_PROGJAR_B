import pygame

class Loss(pygame.sprite.Sprite):
	def __init__(self, img, x, y):
		self.img = img
		self.x = x
		self.y = y

		# collision
		self.rect = pygame.Rect(x, y, 32, 32)

	def getX(self):
		return self.x

	def getY(self):
		return self.y

	def get_hits(self, players):
		hits = []
		for player in players:
			if player.is_alive:
				if self.rect.colliderect(player.rect):
					hits.append(player)
		return hits

	def check_collision(self, players):
		entities = self.get_hits(players)
		for entity in entities:
			entity.is_alive = False

	def update(self, players):
		self.check_collision(players)
		pass

	def render(self, display):
		display.blit(self.img, (self.x, self.y))
