import pygame, os, random
from entities.player import Player
from entities.energy import Energy
from entities.breaks import Break
from entities.loss import Loss
from utils.game_controller import GameController

class Arena():
	def __init__(self, game):
		self.game = game
		self.arena_img = pygame.image.load(os.path.join(self.game.assets_dir,"arena", "arena.png"))
		
		# id game buat unique untuk server nanti
		self.id = None
		
		self.illegal_place = [(5, 5)]
		self.players = []
		self.loss = []
		self.breaks = []
		self.energys = []
		self.num_of_breaks = 12
		self.num_of_energys = 12
		self.num_of_loss = 12

		# player diinisiasi dari server, berapa jumlah orang
		self.players.append(Player(self.game, 0,0,0))
		self.players.append(Player(self.game, 1,320,0))
		self.players.append(Player(self.game, 2,320,320))
		self.players.append(Player(self.game, 3,0,320))

		# generate map permainan
		self.generate_map()

		# game controller, yang berfungsi untuk menghandle game logic dan mendapat data dari server
		self.game_controller = GameController(0)
		self.playerTurn = self.game_controller.getturn()
		self.changeTurn = False
		self.frame = 0

	# update sebagai pengatur nilai object (letak, dls)
	def update(self, delta_time, actions):
		for i in range(self.num_of_breaks):
			self.breaks[i].update(self.players)

		for i in range(self.num_of_energys):
			self.energys[i].update(self.players)
		
		for i in range(self.num_of_loss):
			self.loss[i].update(self.players)

		self.changeTurn = self.players[self.playerTurn].update(delta_time,actions,self.players)
		if self.changeTurn:
			self.game_controller.nextturn()
			self.playerTurn = self.game_controller.getturn()
			if self.players[self.playerTurn].is_alive is False:
				self.playerTurn = self.game_controller.getturn()
			# Kirim flag apapun ke server, menandakan player turn harus berubah
			# ...
			print("kirim ke server pergerakan selesai")

	# render sebagai hasil visual terhadap update object
	def render(self, display):
		display.blit(self.arena_img, (0,0))

		for i in range(self.num_of_breaks):
			self.breaks[i].render(display)

		for i in range(self.num_of_energys):
			self.energys[i].render(display)
		
		for i in range(self.num_of_loss):
			self.loss[i].render(display)

		for player in self.players:
			player.render(display)

	# generate energy and breakas
	def generate_map(self):
		for i in range(self.num_of_energys):
			randX = 5
			randY = 5
			while (randX, randY) in self.illegal_place:
				if i < 3:
					randX = random.randint(1, 5)
					randY = random.randint(1, 5)
				elif i < 6:
					randX = random.randint(5, 9)
					randY = random.randint(1, 5)
				elif i < 9:
					randX = random.randint(1, 5)
					randY = random.randint(5, 9)
				elif i < 12:
					randX = random.randint(5, 9)
					randY = random.randint(5, 9)
			self.energys.append(Energy(pygame.image.load(
				self.game.work_dir + "/assets/energy/energy.png"), randX * 32, randY * 32))
			self.illegal_place.append((randX, randY))

		for i in range(self.num_of_breaks):
			randX = 5
			randY = 5
			while (randX, randY) in self.illegal_place:
				if i < 3:
					randX = random.randint(1, 5)
					randY = random.randint(1, 5)
				elif i < 6:
					randX = random.randint(5, 9)
					randY = random.randint(1, 5)
				elif i < 9:
					randX = random.randint(1, 5)
					randY = random.randint(5, 9)
				elif i < 12:
					randX = random.randint(5, 9)
					randY = random.randint(5, 9)
			self.breaks.append(Break(pygame.image.load(
				self.game.work_dir + "/assets/break/break.png"), randX * 32, randY * 32))
			self.illegal_place.append((randX, randY))

		for i in range(self.num_of_loss):
			randX = 5
			randY = 5
			while (randX, randY) in self.illegal_place:
				if i < 3:
					randX = random.randint(1, 5)
					randY = random.randint(1, 5)
				elif i < 6:
					randX = random.randint(5, 9)
					randY = random.randint(1, 5)
				elif i < 9:
					randX = random.randint(1, 5)
					randY = random.randint(5, 9)
				elif i < 12:
					randX = random.randint(5, 9)
					randY = random.randint(5, 9)
			self.loss.append(Loss(pygame.image.load(
				self.game.work_dir + "/assets/loss/loss.png"), randX * 32, randY * 32))
			self.illegal_place.append((randX, randY))