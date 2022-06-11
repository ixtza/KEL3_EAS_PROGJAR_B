import pygame

class Break(pygame.sprite.Sprite):
	def __init__(self, img, x, y):
		self.img = img
		self.x = x
		self.y = y

		# tricked so that player's stamina whose already fell
		# into the trap becomes negative
		self.tricked = None

		# collision
		self.rect = pygame.Rect(x, y, 32, 32)

	def getX(self):
		return self.x

	def getY(self):
		return self.y

	def get_hits(self, players):
		hits = []
		for player in players:
			if player.is_alive == True:
				if self.rect.colliderect(player.rect):
					if self.tricked != player.id:
						self.tricked = player.id
						player.stamina -= 1
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
		
	def render(self, display):
		display.blit(self.img, (self.x, self.y))
