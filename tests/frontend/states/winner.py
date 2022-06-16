import pygame

class Winner(State):
	def __init__(self, game, text):
		State.__init__(self,game)
		self.text = text

	def update(self, delta_time, actions):
		if actions["action2"]:
			self.exit_state()
		self.game.reset_keys()

	def render(self, display):
		display.fill((255,255,255))
		self.game.draw_text(display, self.text, (0,0,0), self.game.GAME_W/2, self.game.GAME_H/2 )