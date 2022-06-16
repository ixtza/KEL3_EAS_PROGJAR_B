import pygame, os

class Player(pygame.sprite.Sprite):
	def __init__(self, game, id, x, y, turn, conn):
		pygame.sprite.Sprite.__init__(self)

		self.game = game
		self.turn = turn
		self.conn = conn

		self.sprite = os.path.join(self.game.player_dir,"model_move.png")

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
		self.facing = None

		self.newX = 0
		self.newY = 0

		self.currentFrame, self.lastFrameUpdate = 0,0
		self.currentImage = self.animList[0][0]

		# collision
		self.rect = pygame.Rect(x, y, 32, 32)

		# is alive
		self.is_alive = True

		# point
		self.point = 5
			

		self.load_sprites()

		# Flag untuk mengganti giliran player
		self.is_turn = False
		self.doing_server_movement = None
		self.LOGS = {}
		self.stateSync = {
			"x": self.x,
			"y": self.y,
			"facing": self.facing,
			"point": self.point
		}

	def isOutsideArea(self):
		if self.x + self.newX < 0:
			self.x = 0
			print("NOTICE: Invalid Move")
			return True
		if self.x + self.newX > 320:
			self.x = 320
			print("NOTICE: Invalid Move")
			return True
		if self.y + self.newY < 0:
			self.y = 0
			print("NOTICE: Invalid Move")
			return True
		if self.y + self.newY > 320:
			self.y = 320
			print("NOTICE: Invalid Move")
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

	def load_sprites(self):
		for x in range(self.anim):
			self.animList.append([])
			for y in range(self.animStep):
				self.animList[x].append(self.get_image(x,y,32,32,1,(0,0,0)))
	
	def get_image(self, frameX, frameY, width, height, scale, colour):
		image = pygame.Surface((width,height)).convert_alpha()
		image.blit(pygame.image.load(self.sprite), (0,0), ((frameY*width),(frameX*height),width,height))
		image = pygame.transform.scale(image,(width*scale, height*scale))
		image.set_colorkey(colour)
		return image

	def update(self, deltaTime, actions, players):
		if self.is_alive:
			change = self.check_movement(actions)
			self.check_collision(players)
			self.animate(deltaTime)
			# if self.conn.our_player_turn == self.turn and self.moving == False and self.stateSync["facing"] != None and (
			# 	self.x != self.stateSync["x"]
			# 	or self.y != self.stateSync["y"]
			# 	or self.facing != self.stateSync["facing"]
			# 	or self.point != self.stateSync["point"]
			# ):
			# 	self.stateSync = {
			# 		"x": self.x,
			# 		"y": self.y,
			# 		"facing": self.facing,
			# 		"point": self.point
			# 	}
			# 	self.conn.syncPlayer(self.stateSync)
			return change
		if self.is_alive == False:
			self.animMode = 0
			self.currentFrame = 0
			self.point = 0
			return True

	def render(self, display):
		if self.newX == 0 and self.newY == 0:
			# if self.conn.our_player_turn != self.turn and (
			# 	self.x != self.stateSync["x"]
			# 	or self.y != self.stateSync["y"]
			# 	or self.facing != self.stateSync["facing"]
			# 	or self.point != self.stateSync["point"]
			# ):
			# 	self.x = self.stateSync["x"]
			# 	self.y = self.stateSync["y"]
			# 	self.facing = self.stateSync["facing"]
			# 	self.point = self.stateSync["point"]

			self.moving = False
			display.blit(self.animList[self.animMode][self.currentFrame], (self.x,self.y))
			return True if self.is_turn else False # animasi selesai

		display.blit(self.animList[self.animMode][self.currentFrame], (self.x,self.y))
		return False # tidak ada animasi atau animasi belum selesai

	def alive(self):
		if self.point < 1:
			self.is_alive = False

	def check_movement(self, actions, from_server=False):

		if (self.conn.our_player_turn == self.turn or from_server) and actions['keydown'] == True and self.moving == False and self.is_turn == False:
			self.moving = True
			if from_server: self.doing_server_movement = True
			if actions['left'] == True:
				self.point -= 1
				self.facing = 'left'
				self.animMode = 2
				self.newX -= 32
			elif actions['right'] == True:
				self.point -= 1
				self.facing = 'right'
				self.animMode = 3
				self.newX += 32
			elif actions['up'] == True:
				self.point -= 1
				self.facing = 'up'
				self.animMode = 1
				self.newY -= 32
			elif actions['down'] == True:
				self.point -= 1
				self.facing = 'down'
				self.animMode = 4
				self.newY += 32
			if self.isOutsideArea():
				self.point += 1
				self.newX = 0
				self.newY = 0
				self.is_turn = False
				return False

			self.is_turn = True

			if self.conn.our_player_turn == self.turn and self.facing != None:
				self.conn.sendAction(self.facing)
			return False


		if (actions['keyup'] == True or self.doing_server_movement or self.is_alive == False) and self.moving == False:
			"""
			Setelah melepas tombol gerakan, kirim data gerakan ke seluruh pemain
			"""

			self.doing_server_movement = False
			self.facing = None
			self.newX = 0
			self.newY = 0
			if self.is_turn == True:
				self.alive()
				self.is_turn = False
				return True
		return False
	
	def get_hits(self, players):
		hits = []
		for player in players:
			if player.id != self.getId():
				if self.rect.colliderect(player.rect):
					hits.append(player)
		return hits

	def check_collision(self, players):
		collisions = self.get_hits(players)
		for tile in collisions:
			if self.facing == 'right':
				self.newX -= 32
			elif self.facing == 'left':
				self.newX += 32
			elif self.facing == 'up':
				self.newY += 32
			elif self.facing == 'down':
				self.newY -= 32

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
		if self.lastFrameUpdate > .1:
			self.lastFrameUpdate = 0
			self.currentFrame = (self.currentFrame +1) % self.animStep
		
		# Update player rect
		self.rect.update(self.x,self.y,32,32)
		# print("animate: " + str((self.newX, self.newY)))

	def syncFromServer(self, state):
		print(str(self.turn) + " got sync: " + str(state))
		self.stateSync = state