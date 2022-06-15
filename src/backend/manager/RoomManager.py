# import threading

# Chat dkk di sini tempatnya
# class RoomManager(threading.Thread):
class RoomManager():
	def __init__(self):
		self.players = {}

		# [0] -> player, [1] -> arena, [2] -> player_ready, [3] -> turn, [4] -> player coordinate data
		self.gameRoom = {}
		self.gameRoomId = 1

	def addPlayer(self, player):
		self.players[player.id] = [player]
		if (self.gameRoomId in self.gameRoom) and len(self.gameRoom[self.gameRoomId][0]) < 4:
			self.gameRoom[self.gameRoomId][0].append(player.id)
		else:
			if (self.gameRoomId in self.gameRoom) and len(self.gameRoom[self.gameRoomId][0]) >= 4:
				self.gameRoomId += 1
			self.gameRoom[self.gameRoomId] = [[player.id], [], {}, 1]
		turn = len(self.gameRoom[self.gameRoomId][0])

		player.sendResponse(['your_turn', None, turn])
		player.turn = turn
		self.broadcastToRoom('player_enter', [player.id, turn], self.gameRoomId, player.id)
		for i in range(0, len(self.gameRoom[self.gameRoomId][0])):
			uid = self.gameRoom[self.gameRoomId][0][i]
			if uid == player.id: continue
			print("send player_enter to player " + str(i + 1))
			player.sendResponse(['player_enter', None, [uid, i + 1]])

		self.players[player.id].append(self.gameRoomId)
		# print('added player: ' + str(self.players[player.id]))
		# print(str(self.players))
		# print(str(self.gameRoom))

	def removePlayer(self, player):
		roomId = self.players.get(player.id)
		if not roomId: return
		roomId = roomId[1]
		self.broadcastToRoom('end_game', ['player_leave', player.id], roomId)

		# Leave = exit game
		for uid in self.gameRoom[roomId][0]:
			player = self.players.get(uid)
			if not player: return
			player = player[0]
			del self.players[uid]
			player.stop(True)

		del self.gameRoom[roomId]
		print(str(self.players))
		print(str(self.gameRoom))

	def addArenaConfig(self, player, arena_config):
		roomId = self.players.get(player.id)
		if not roomId: return
		roomId = roomId[1]
		self.gameRoom[roomId][1].append(arena_config)
		self.broadcastToRoom('broadcast_arena_config', arena_config, roomId, player.id)
		print("BROADCASTED ARENA CONFIG")

	def resendArenaConfig(self, player):
		pass

	def playerReady(self, player):
		roomId = self.players.get(player.id)
		if not roomId: return
		roomId = roomId[1]
		self.gameRoom[roomId][2][player.id] = True
		print("player " + player.id + " ready")

	def roomReady(self, player):
		roomId = self.players.get(player.id)
		if not roomId: return
		roomId = roomId[1]
		return len(self.gameRoom[roomId][2]) >= 4

	def sendAllPlayerReady(self, player):
		roomId = self.players.get(player.id)
		if not roomId: return
		roomId = roomId[1]
		if self.roomReady(player):
			self.gameRoom[roomId][2] = {}
			self.gameRoom[roomId][3] += 1
			if self.gameRoom[roomId][3] > 4: self.gameRoom[roomId][3] = 1
			self.broadcastToRoom('all_player_ready', None, roomId)
			print("all player ready")

	def sendTurn(self, player):
		roomId = self.players.get(player.id)
		if not roomId: return
		roomId = roomId[1]
		player.sendResponse(["player_turn", None, self.gameRoom[roomId][3]])
		# print("send turn ")
		pass

	def broadcastAction(self, player, action):
		roomId = self.players.get(player.id)
		if not roomId: return
		roomId = roomId[1]
		self.broadcastToRoom('player_action', action, roomId, player.id)

	def broadcastToRoom(self, kind, msg, roomId, playerId=None):
		# playerId None = Server
		res = [kind, playerId, msg]
		for uid in self.gameRoom[roomId][0]:
			if uid == playerId: continue
			player = self.players.get(uid)
			if not player: return
			player = player[0]
			player.sendResponse(res)

	def broadcastToAll(self, kind, msg, playerId=None):
		# playerId None = Server
		res = [kind, playerId, msg]
		for uid in self.players:
			if uid == playerId: continue
			self.players[uid][0].sendResponse(res)

	def playerMove(self, playerId, moveX, moveY):
		roomId = self.players.get(playerId)
		if not roomId: return
		roomId = roomId[1]
		self.broadcastToRoom('move', [moveX, moveY], roomId, playerId)

	def playerChat(self, playerId, msg):
		roomId = self.players.get(playerId)
		if not roomId: return
		roomId = roomId[1]
		self.broadcastToRoom('chat', msg, roomId, playerId)

	def stop(self):
		self.running = False
		# self._stop_event.set()

	def stopped(self):
		# return self._stop_event.is_set()
		return self.running