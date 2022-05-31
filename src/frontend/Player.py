import pygame


class Player:

	point = 7

	def __init__(self, img, id, x, y):
		self.img = img
		self.id = id
		self.x = x
		self.y = y
		self.currentFrame, self.lastFrameUpdate = 0,0
		self.anim = 5
		self.animList = []
		self.animMode = 0
		self.animState = 0
		self.animStep = 7
		self.animCooldown = 200
		self.load_sprites()
		self.newX = 0
		self.newY = 0

	def print(self, screen):
		screen.blit(self.img, (self.x, self.y))

	def move(self, x, y):
		self.x = self.x + x
		self.y = self.y + y

	def check_movement(self, event):
		pressed = False
		if event.type == pygame.KEYDOWN and pressed == False:
			pressed = True
			if event.key == pygame.K_LEFT:
				self.move(-32, 0)
			if event.key == pygame.K_RIGHT:
				self.move(32, 0)
			if event.key == pygame.K_UP:
				self.move(0, -32)
			if event.key == pygame.K_DOWN:
				self.move(0, 32)
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

	def render(self, display):
		# for i in range (self.x,self.newX+1):
		# 	self.x = i
		# 	display.blit(self.animList[self.animMode][self.currentFrame], (self.x,self.y))
		# for j in range (self.y,self.newY+1):
		# 	self.y = j
		# 	display.blit(self.animList[self.animMode][self.currentFrame], (self.x,self.y))
		display.blit(self.animList[self.animMode][self.currentFrame], (self.x,self.y))

	def animate(self, deltaTime, directionX, directionY):
		# Compute how much time has passed since the frame last updated
		self.lastFrameUpdate += deltaTime
		# If no direction is pressed, set image to idle and return
		if not (directionX or directionY): 
			self.animMode = 0
			self.currentFrame = 0
			return
		# If an image was pressed, use the appropriate list of frames according to direction
		if directionX:
			if directionX > 0: self.animMode = 2
			else: self.animMode = 3
		if directionY:
			if directionY > 0: self.animMode = 1
			else: self.animMode = 4
		# Advance the animation if enough time has elapsed
		if self.lastFrameUpdate > .15:
			self.lastFrameUpdate = 0
			self.currentFrame = (self.currentFrame +1) % len(self.animStep)
			
	def load_sprites(self):
		for x in range(self.anim):
			self.animList.append([])
			for y in range(self.animStep):
				self.animList[x].append(self.get_image(x,y,32,32,1,(0,0,0)))

	def get_image(self, frameX, frameY, width, height, scale, colour):
		image = pygame.Surface((width,height)).convert_alpha()
		image.blit(self.img, (0,0), ((frameX*width),(frameY*height),width,height))
		image = pygame.transform.scale(image,(width*scale, height*scale))
		image.set_colorkey(colour)
		return image
