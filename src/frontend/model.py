import pygame

class SpriteModel():
	def __init__(self,image):
		self.model = image

	def get_image(self, frameX, frameY, width, height, scale, colour):
		image = pygame.Surface((width,height)).convert_alpha()
		image.blit(self.model, (0,0), ((frameX*width),(frameY*height),width,height))
		image = pygame.transform.scale(image,(width*scale, height*scale))
		image.set_colorkey(colour)

		return image