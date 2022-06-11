import pygame
from states.state import State
from entities.arena import Arena

class Game_World(State):
	def __init__(self, game):
		State.__init__(self,game)

		# inisiasi map sebagai list room
		self.arenas = []
		self.arenas.append(Arena(self.game))

	# update sebagai pengatur nilai object (letak, dls)
	def update(self, delta_time, actions):
		for arena in self.arenas:
			arena.update(delta_time, actions)

	
	# render sebagai hasil visual terhadap update object
	def render(self, display):
		for arena in self.arenas:
			arena.render(display)

	