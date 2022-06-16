import pygame, os, random
from entities.player import Player
from entities.energy import Energy
from entities.breaks import Break
from entities.loss import Loss
from utils.game_controller import GameController
from utils.score_board import Text

class Arena():
	def __init__(self, game, conn):
		self.conn = conn
		self.game = game
		self.arena_img = pygame.image.load(os.path.join(self.game.assets_dir,"arena", "arena.png"))
		self.game_controller = GameController(self.conn)
		
		if not self.conn.isRoomHost():
			arena_configuration = self.conn.getArenaConfig()
		else:
			arena_configuration = {
				"id": None,
				"illegal_place": [(5, 5)],
				"players": [(0,0),(0,320),(320,0),(320,320)],
				"loss": None,
				"breaks": None,
				"energys": None,
				# "num_of_breaks": 0,
				# "num_of_energys": 0,
				# "num_of_loss": 0,
				"num_of_breaks": 12,
				"num_of_energys": 12,
				"num_of_loss": 12,
			}

		# id game buat unique untuk server nanti
		self.id = arena_configuration["id"]

		self.illegal_place 	= arena_configuration["illegal_place"]
		self.players 	   	= []
		self.loss 		   	= []
		self.breaks 	   	= []
		self.energys 	   	= []
		self.num_of_breaks 	= arena_configuration["num_of_breaks"]
		self.num_of_energys	= arena_configuration["num_of_energys"]
		self.num_of_loss 	= arena_configuration["num_of_loss"]
		
		players_id_turn_data = self.conn.getAllPlayersIdTurn()
		players_id_turn_data_uid = list(players_id_turn_data.keys())
		for i in range(0, len(players_id_turn_data)):
			uid = players_id_turn_data_uid[i]
			turn = players_id_turn_data[uid]["turn"]
			p = arena_configuration["players"][turn - 1]
			player = Player(self.game, uid,p[0],p[1], turn, self.conn)
			self.players.insert(turn - 1, player)
			players_id_turn_data[uid]["object"] = player

		# generate map permainan
		if self.conn.isRoomHost():
			# player diinisiasi dari server, berapa jumlah orang

			self.generate_map()
			arena_configuration["loss"] = [(l.x // 32, l.y // 32) for l in self.loss]
			arena_configuration["breaks"] = [(b.x // 32, b.y // 32) for b in self.breaks]
			arena_configuration["energys"] = [(e.x // 32, e.y // 32) for e in self.energys]
			with open("./arena_config", 'w') as f:
				f.write(str(arena_configuration))
				f.close()

			self.conn.broadcastArenaConfig(arena_configuration)
		else:
			for l in arena_configuration["loss"]:
				self.loss.append(Loss(pygame.image.load(
					self.game.work_dir + "/assets/loss/loss.png"), l[0] * 32, l[1] * 32, self.conn))

			for b in arena_configuration["breaks"]:
				self.breaks.append(Break(pygame.image.load(
					self.game.work_dir + "/assets/break/break.png"), b[0] * 32, b[1] * 32, self.conn))

			for e in arena_configuration["energys"]:
				self.energys.append(Energy(pygame.image.load(
					self.game.work_dir + "/assets/energy/energy.png"), e[0] * 32, e[1] * 32, self.conn))

		# game controller, yang berfungsi untuk menghandle game logic dan mendapat data dari server
		self.playerTurn = self.game_controller.getturn()
		self.changeTurn = False
		self.frame = 0

		# socre board text position
		self.text = Text(os.path.join(self.game.font_dir, "ROCK.ttf"),14)

		# finish line
		self.finish = False
		self.ongoing = True

		# set window title
		if self.conn.our_player_turn == 0:
			pygame.display.set_caption('Tap Treasure - Player ' + str(self.conn.our_player_turn) + " - Your Turn")
		else:
			pygame.display.set_caption('Tap Treasure - Player ' + str(self.conn.our_player_turn))

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
			# os.system('cls')
			# print("Current Turn: "+ str(self.playerTurn+1) +"\nCurrent score status: \n"
			#                     'Player '+ str(self.players[0].id) + ' :' + str(self.players[0].getPoint()) + '-' + str(self.players[0].is_alive) + "\n"
			#                     'Player '+ str(self.players[1].id) + ' :' + str(self.players[1].getPoint()) + '-' + str(self.players[1].is_alive) + "\n"
			#                     'Player '+ str(self.players[2].id) + ' :' + str(self.players[2].getPoint()) + '-' + str(self.players[2].is_alive) + "\n"
			#                     'Player '+ str(self.players[3].id) + ' :' + str(self.players[3].getPoint()) + '-' + str(self.players[3].is_alive) 
			# )

# cek apakah player sekarang sudah mencapai lokasi finish, jika iya permainan berakhir

			if self.check_finish(self.players[self.playerTurn]):
				print('Player '+str(self.players[self.playerTurn].id)+' menang!')
				if self.playerTurn+1 == self.conn.our_player_turn:
					print("NOTICE: your win")
					pygame.display.set_caption('Tap Treasure - Player ' + str(self.conn.our_player_turn) + " - You Win")
				for player in self.players:
					player.is_alive = False
				# kirim tanda apapun bahwa game telah berakhir
				# ...
			else:
				print(self.playerTurn)
				self.playerTurn = self.game_controller.getturn()
				if self.players[self.playerTurn].is_alive == False:
					self.game_controller.addEliminated(self.players[self.playerTurn].id)
					if len(self.game_controller.getEliminated()) == 4:
						self.ongoing = False
						pygame.display.set_caption('Tap Treasure - Player ' + str(self.conn.our_player_turn) + " - Draw")
						print('permainan berakhir')

				# Kirim flag apapun ke server, menandakan player turn harus berubah
				# ...
				# print("kirim ke server pergerakan selesai")

			# mengganti turn player, ketika is_alive player false, maka akan langsung otomastis switch ke giliran selanjutnya
			if self.playerTurn+1 == self.conn.our_player_turn:
				print((self.players[self.playerTurn].x, self.players[self.playerTurn].y))
			print("NOTICE: this player ready")
			# self.conn.sendReady()
			self.conn.waitAllPlayerReady(self.players[self.conn.our_player_turn - 1].is_alive)
			print("NOTICE: all player ready")
			self.playerTurn = self.game_controller.getturn()

			if self.playerTurn+1 == self.conn.our_player_turn and self.ongoing:
				print("NOTICE: your turn")
				pygame.display.set_caption('Tap Treasure - Player ' + str(self.conn.our_player_turn) + " - Your Turn")
			elif self.ongoing:
				pygame.display.set_caption('Tap Treasure - Player ' + str(self.conn.our_player_turn))

			# if self.players[self.playerTurn].is_alive == False:
			# 	self.game_controller.addEliminated(self.players[self.playerTurn].turn)
			# 	if len(self.game_controller.getEliminated()) == 4:
			# 		print('NOTICE: permainan berakhir, seluruh pemain kecapaian')
			# 		self.game.force_exit()
			
	# finish sebagai salah satu cara akhir dari permainan
	def check_finish(self, player):
		if player.x in range(159,192) and player.y in range(159,192):
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
			self.text.render(display, "P-" + str(player.turn) + " Score :" + str(player.getPoint()),440, (player.turn+1) * 15 + 25)
		
		# for player in self.players:
		# 	self.text.render(display, "P-" + str(player.getId()) + " Score :" + str(player.getPoint()),420, ((player.getId()+1) * 15)+25)

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
				self.game.work_dir + "/assets/energy/energy.png"), randX * 32, randY * 32, self.conn))
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
				self.game.work_dir + "/assets/break/break.png"), randX * 32, randY * 32, self.conn))
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
				self.game.work_dir + "/assets/loss/loss.png"), randX * 32, randY * 32, self.conn))
			self.illegal_place.append((randX, randY))