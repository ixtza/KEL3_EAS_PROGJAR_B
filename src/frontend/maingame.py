import pygame
import random

#initialize the pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((352,416))

#title and icon
pygame.display.set_caption("Tap Treasure")
icon = pygame.image.load("assets/icon/treasure.png")
pygame.display.set_icon(icon)

#arena
arenaImg = pygame.image.load("assets/arena/arena.png")
arenaX = 0
arenaY = 0

def Arena(x,y):
	screen.blit(arenaImg,(x,y))

#gameloop
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	#RGB Red, Green, Blue
	screen.fill((0,255,0))

	Arena(arenaX,arenaY)
	pygame.display.update()