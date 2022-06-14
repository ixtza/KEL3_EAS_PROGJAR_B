import pygame

class Break(pygame.sprite.Sprite):
	def __init__(self, img, x, y):
		self.img = img
		self.x = x
		self.y = y

		# tricked so that player's point whose already fell
		# into the trap becomes negative
		self.tricked = None

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
			if player.is_alive and player.x is self.x and player.y is self.y:
				self.is_passed = True
				if self.rect.colliderect(player.rect):
					if self.tricked != player.id:
						self.tricked = player.id
						player.point -= 1
					hits.append(player)
		return hits

	def check_collision(self, players):
		entities = self.get_hits(players)
		for entity in entities:
			if entity.facing == 'right':
				entity.newX = -1
			elif entity.facing == 'left':
				entity.newX = +1
			elif entity.facing == 'up':
				entity.newY = +1
			elif entity.facing == 'down':
				entity.newY = -1

	def update(self, players):
		self.check_collision(players)
		pass
		
	def render(self, display):
		if self.is_passed:
			display.blit(self.img, (self.x, self.y))
