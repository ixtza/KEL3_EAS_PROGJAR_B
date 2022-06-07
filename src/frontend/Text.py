import pygame

class Text:

	def __init__(self, font):
		self.font = pygame.font.Font(font, 16)

	def print(self, screen, text, x, y):
		text = self.font.render(text, True, (255, 0, 0))
		textRect = text.get_rect()
		textRect.center = (x, y)
		screen.blit(text, textRect)