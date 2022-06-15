import pygame

class Loss(pygame.sprite.Sprite):
	def __init__(self, img, x, y, conn):
		self.img = img
		self.x = x
		self.y = y
		self.conn = conn

		# collision
		self.rect = pygame.Rect(x, y, 32, 32)
		self.is_passed = False

	def getX(self):
		return self.x

	def getY(self):
		return self.y

	def get_hits(self, players):
		hits = []
		for player in players:
			# cek ketika sudah di koordinatnya
			if player.is_alive and player.x == self.x and player.y == self.y:
				self.is_passed = True
				print(player.id)
				# if self.rect.colliderect(player.rect):
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
		if self.is_passed:
			display.blit(self.img, (self.x, self.y))
