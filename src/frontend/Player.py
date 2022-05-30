import pygame

class Player:

	point = 7

	def __init__(self, img, id, x, y):
		self.img = img
		self.id = id
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
			if self.isOutsideArea():
				return False
			return True
		if event.type == pygame.KEYUP:
			pressed = False
		return False

	def isOutsideArea(self):
		if self.x < 0:
			self.x = 0
			print("Invalid Move")
			return True
		if self.x > 320:
			self.x = 320
			print("Invalid Move")
			return True
		if self.y < 0:
			self.y = 0
			print("Invalid Move")
			return True
		if self.y > 320:
			self.y = 320
			print("Invalid Move")
			return True

	def getPoint(self):
		return self.point

	def setPoint(self, point):
		self.point = point

	def getX(self):
		return self.x
	
	def getY(self):
		return self.y

	def getId(self):
		return self.id