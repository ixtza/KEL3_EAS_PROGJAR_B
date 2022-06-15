# import threading

# Chat dkk di sini tempatnya
# class RoomManager(threading.Thread):
class RoomManager():
	def __init__(self):
		self.players = {}
		self.gameRoom = {}
		self.gameRoomId = 1

	def addPlayer(self, player):
		self.players[player.id] = [player]
		if (self.gameRoomId in self.gameRoom) and len(self.gameRoom[self.gameRoomId]) < 4:
			self.gameRoom[self.gameRoomId].append(player.id)
		else:
			if (self.gameRoomId in self.gameRoom) and len(self.gameRoom[self.gameRoomId]) >= 4:
				self.gameRoomId += 1
			self.gameRoom[self.gameRoomId] = [player.id]
		player.sendResponse(['your_turn', None, len(self.gameRoom[self.gameRoomId])])
		self.players[player.id].append(self.gameRoomId)
		print('added player: ' + str(self.players[player.id]))
		print(str(self.players))
		print(str(self.gameRoom))

	def removePlayer(self, player):
		roomId = self.players.get(player.id)
		if not roomId: return
		roomId = roomId[1]
		self.broadcastToRoom('end_game', ['player_leave', player.id], roomId)

		# Leave = exit game
		for uid in self.gameRoom[roomId]:
			player = self.players.get(uid)
			if not player: return
			player = player[0]
			del self.players[uid]
			player.stop(True)

		del self.gameRoom[roomId]
		print(str(self.players))
		print(str(self.gameRoom))

	def broadcastToRoom(self, kind, msg, roomId, playerId=None):
		# playerId None = Server
		res = [kind, playerId, msg]
		for uid in self.gameRoom[roomId]:
			if uid == playerId: continue
			player = self.players.get(uid)
			if not player: return
			player = player[0]
			player.sendResponse(res)

	def broadcastToAll(self, kind, msg, playerId=None):
		# playerId None = Server
		res = [kind, playerId, msg]
		for uid in self.players:
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