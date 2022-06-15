import pygame, os, random
from entities.player import Player
from entities.energy import Energy
from entities.breaks import Break
from entities.loss import Loss
from utils.game_controller import GameController
from utils.score_board import Text

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

		# socre board text position
		self.text = Text(os.path.join(self.game.font_dir, "ROCK.ttf"),14)

		# finish line
		self.finishLine = (160,160)
		self.finish = False
		self.ongoing = True

	# update sebagai pengatur nilai object (letak, dls)
	def update(self, delta_time, actions):
		for i in range(self.num_of_breaks):
			self.breaks[i].update(self.players)

		for i in range(self.num_of_energys):
			self.energys[i].update(self.players)
		
		for i in range(self.num_of_loss):
			self.loss[i].update(self.players)

		self.changeTurn = self.players[self.playerTurn].update(delta_time,actions,self.players)
		if self.changeTurn and self.ongoing:
			os.system('cls')
			print("Current Turn: "+ str(self.playerTurn+1) +"\nCurrent score status: \n"
			                    'Player '+ str(self.players[0].id) + ' :' + str(self.players[0].getPoint()) + '-' + str(self.players[0].is_alive) + "\n"
			                    'Player '+ str(self.players[1].id) + ' :' + str(self.players[1].getPoint()) + '-' + str(self.players[1].is_alive) + "\n"
			                    'Player '+ str(self.players[2].id) + ' :' + str(self.players[2].getPoint()) + '-' + str(self.players[2].is_alive) + "\n"
			                    'Player '+ str(self.players[3].id) + ' :' + str(self.players[3].getPoint()) + '-' + str(self.players[3].is_alive) 
			)
			# mengganti turn player, ketika is_alive player false, maka akan langsung otomastis switch ke giliran selanjutnya

			# cek apakah player sekarang sudah mencapai lokasi finish, jika iya permainan berakhir

			if self.check_finish(self.players[self.playerTurn]):
				print('Player '+str(self.players[self.playerTurn].id)+' menang!')
				for player in self.players:
					player.is_alive = False
				# kirim tanda apapun bahwa game telah berakhir
				# ...
			else:
				print(self.playerTurn)
				self.game_controller.nextturn()
				self.playerTurn = self.game_controller.getturn()
				if self.players[self.playerTurn].is_alive == False:
					self.game_controller.addEliminated(self.players[self.playerTurn].id)
					if len(self.game_controller.getEliminated()) == 4:
						print('permainan berakhir')

				# Kirim flag apapun ke server, menandakan player turn harus berubah
				# ...
				# print("kirim ke server pergerakan selesai")

	# finish sebagai salah satu cara akhir dari permainan
	def check_finish(self, player):
		if (player.x, player.y) == self.finishLine:
			self.finish = True
			self.ongoing = False
		return self.finish
	
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
		
		for player in self.players:
			self.text.render(display, "P-" + str(player.getId()) + " Score :" + str(player.getPoint()),420, ((player.getId()+1) * 15)+25)

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