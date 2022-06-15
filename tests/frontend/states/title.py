from states.state import State
from states.game_world import Game_World

class Title(State):
	def __init__(self, game, conn):
		State.__init__(self, game, conn)

	def update(self, delta_time, actions):
		play_signal = self.conn.waitAllPlayers()
		if play_signal:
			new_state = Game_World(self.game,self.conn)
			new_state.enter_state()
			self.game.reset_keys()
		else: self.game.force_exit()

	def render(self, display):
		display.fill((255,255,255))
		self.game.draw_text(display, "Tap Treasure", (0,0,0), self.game.GAME_W/2, self.game.GAME_H/2 )