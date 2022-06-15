import pygame
import os

class Text:

	def __init__(self, font, size):
		self.font = pygame.font.Font(font, size)
		self.text = None

	def print(self, display, text, x, y):
		self.text = self.font.render(text, True, (255, 0, 0))
		textRect = self.text.get_rect()
		textRect.center = (x, y)
		display.blit(self.text, textRect)