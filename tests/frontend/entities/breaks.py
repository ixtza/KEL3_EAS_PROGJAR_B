import pygame

class Break(pygame.sprite.Sprite):
	def __init__(self, img, x, y, conn):
		self.img = img
		self.x = x
		self.y = y
		self.conn = conn

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
			if player.is_alive and player.x == self.x and player.y == self.y:
				self.is_passed = True
				if self.rect.colliderect(player.rect):
					if self.tricked != player.id:
						self.tricked = player.id
						player.point -= 1
						print(str(player.turn) + " tricked, loss point")
					hits.append(player)
		return hits

	def check_collision(self, players):
		entities = self.get_hits(players)
		"""
		penyebab desync, biarkan player keluar dari break sendiri
		"""
		# for entity in entities:
		# 	if entity.facing == 'right':
		# 		entity.newX = -32
		# 		print(str(entity.turn) + " tricked, moved to right")
		# 	elif entity.facing == 'left':
		# 		entity.newX = 32
		# 		print(str(entity.turn) + " tricked, moved to left")
		# 	elif entity.facing == 'up':
		# 		entity.newY = 32
		# 		print(str(entity.turn) + " tricked, moved to up")
		# 	elif entity.facing == 'down':
		# 		entity.newY = -32
		# 		print(str(entity.turn) + " tricked, moved to down")

	def update(self, players):
		self.check_collision(players)
		pass
		
	def render(self, display):
		# if self.is_passed:
		# 	display.blit(self.img, (self.x, self.y))
		display.blit(self.img, (self.x, self.y))
