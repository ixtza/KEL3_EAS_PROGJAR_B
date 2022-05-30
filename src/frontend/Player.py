import pygame

class Player:
	def __init__(self, img, x, y):
		self.img = img
		self.x = x
		self.y = y

	def print(self, screen):
		screen.blit(self.img,(self.x, self.y))

	def move(self,x,y):
		self.x = self.x + x
		self.y = self.y + y

	def check_movement(self, event):
		pressed = False
		if event.type == pygame.KEYDOWN and pressed == False:
			pressed = True
			if event.key == pygame.K_LEFT:
				self.move(-32,0)
			if event.key == pygame.K_RIGHT:
				self.move(32,0)
			if event.key == pygame.K_UP:
				self.move(0,-32)
			if event.key == pygame.K_DOWN:
				self.move(0,32)
		if event.type == pygame.KEYUP:
			pressed = False

		if self.x < 0:
			self.x = 0
		if self.x > 352:
			self.x = 352
		if self.y < 0:
			self.y = 352
		if self.y > 352:
			self.y = 352
