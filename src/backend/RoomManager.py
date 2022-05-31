# import threading

# Chat dkk di sini tempatnya
# class RoomManager(threading.Thread):
class RoomManager():
	def __init__(self):
		# threading.Thread.__init__(self)
		self.players = {}
		self.gameRoom = {}
		self.gameRoomId = 1

	def addPlayer(self, player):
		if not self.running: return
		self.players[player.id] = [player]
		if (self.gameRoomId in self.gameRoom) and len(self.gameRoom[self.gameRoomId]) < 4:
			self.gameRoom[self.gameRoomId].append(player.id)
		else:
			self.gameRoomId += 1
			self.gameRoom[self.gameRoomId] = [player.id]

	def removePlayer(self, player):
		if not self.running: return
		roomId = self.players[player.id][1]
		self.broadcastToRoom('end_session', ['player_leave', player.id])

		# TODO Leave = exit game ?
		for uid in self.gameRoom[roomId]:
			player = self.players[uid][0]
			del self.players[uid]
			if uid == player.id: continue
			player.stop(True)

	def broadcastToRoom(self, kind, msg, playerId=None):
		# playerId None = Server
		if not self.running: return
		res = [kind, playerId, msg]
		for uid in self.gameRoom[self.players[playerId][1]]:
			if uid == playerId: continue
			self.player[uid].sendResponse(res)

	def broadcastToAll(self, kind, msg, playerId=None):
		# playerId None = Server
		if not self.running: return
		res = [kind, playerId, msg]
		for uid in self.players:
			self.player[uid].sendResponse(res)

	def playerMove(self, playerId, moveX, moveY):
		if not self.running: return
		self.broadcastToRoom('move', [moveX, moveY], playerId)

	def playerChat(self, playerId, msg):
		if not self.running: return
		self.broadcastToRoom('chat', msg, playerId)

	def stop(self):
		self.running = False
		# self._stop_event.set()

	def stopped(self):
		# return self._stop_event.is_set()
		return self.running