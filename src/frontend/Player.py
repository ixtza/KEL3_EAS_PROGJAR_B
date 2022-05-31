import pygame


class Player(pygame.sprite.Sprite):

	point = 7

	def __init__(self, img, id, x, y):
		self.img = img
		self.id = id
		self.x = x
		self.y = y

		self.anim = 5
		self.animList = []
		self.animMode = 0
		self.animState = 0
		self.animStep = 7
		self.animCooldown = 200
		self.load_sprites()
		self.moving = False

		self.newX = 0
		self.newY = 0

		self.currentFrame, self.lastFrameUpdate = 0,0
		self.currentImage = self.animList[0][0]

	# def move(self, x, y):
	# 	pass
	# 	self.x = self.x + x
	# 	self.y = self.y + y

	def check_movement(self, event):
		pressed = False
		if event.type == pygame.KEYDOWN and pressed == False and self.moving == False:
			pressed = True
			self.moving = True
			if event.key == pygame.K_LEFT:
				self.animMode = 2
				# self.move(-32, 0)
				self.newX = -32
			if event.key == pygame.K_RIGHT:
				self.animMode = 3
				# self.move(32, 0)
				self.newX = 32
			if event.key == pygame.K_UP:
				self.animMode = 1
				# self.move(0, -32)
				self.newY = -32
			if event.key == pygame.K_DOWN:
				self.animMode = 4
				# self.move(0, 32)
				self.newY = 32
			if self.isOutsideArea():
				self.newX = 0
				self.newY = 0
				return False
			return True
		if event.type == pygame.KEYUP and self.moving == False:
			# self.animMode = 0
			self.newX = 0
			self.newY = 0
			pressed = False
		return False

	def isOutsideArea(self):
		if self.x + self.newX < 0:
			self.x = 0
			print("Invalid Move")
			return True
		if self.x + self.newX > 320:
			self.x = 320
			print("Invalid Move")
			return True
		if self.y + self.newY < 0:
			self.y = 0
			print("Invalid Move")
			return True
		if self.y + self.newY > 320:
			self.y = 320
			print("Invalid Move")
			return True
		return False

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
		if self.newX == 0 and self.newY == 0:
			self.moving = False
		display.blit(self.animList[self.animMode][self.currentFrame], (self.x,self.y))

	def update(self, deltaTime):
		self.animate(deltaTime)

	def animate(self, deltaTime):
		# Compute how much time has passed since the frame last updated
		self.lastFrameUpdate += deltaTime
		# If no direction is pressed, set image to idle and return
		if not (self.newX or self.newY): 
			# self.animMode = 0
			self.currentFrame = 0
			return
		# If an image was pressed, use the appropriate list of frames according to direction
		if self.newX and self.isOutsideArea()!=True:
			if self.newX > 0: 
				self.animMode = 2
				self.x+=1
				self.newX-=1
			else: 
				self.animMode = 3
				self.x-=1
				self.newX+=1
		if self.newY and self.isOutsideArea()!=True:
			if self.newY > 0: 
				self.animMode = 1
				self.y+=1
				self.newY-=1
			else: 
				self.animMode = 4
				self.y-=1
				self.newY+=1
		# Advance the animation if enough time has elapsed
		if self.lastFrameUpdate > .15:
			self.lastFrameUpdate = 0
			self.currentFrame = (self.currentFrame +1) % self.animStep
			
	def load_sprites(self):
		for x in range(self.anim):
			self.animList.append([])
			for y in range(self.animStep):
				self.animList[x].append(self.get_image(x,y,32,32,1,(0,0,0)))

	def get_image(self, frameX, frameY, width, height, scale, colour):
		image = pygame.Surface((width,height)).convert_alpha()
		image.blit(self.img, (0,0), ((frameY*width),(frameX*height),width,height))
		image = pygame.transform.scale(image,(width*scale, height*scale))
		image.set_colorkey(colour)
		return image
