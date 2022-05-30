import pygame

#importing game classes
import Player
import Arena

import os 

#working directory path
work_dir = os.path.dirname(os.path.realpath(__file__))

#initialize the pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((352,416))

#title and icon
pygame.display.set_caption("Tap Treasure")
icon = pygame.image.load(work_dir+"/assets/icon/treasure.png")
pygame.display.set_icon(icon)

#arena
arena = Arena.Arena(pygame.image.load(work_dir+"/assets/arena/arena.png"), 0, 0)
arena.generate_map()

#players
player1 = Player.Player(pygame.image.load(work_dir+"/assets/player/player1.png"), 0, 320)

#keyboard
pressed = False

#gameloop
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		player1.check_movement(event)
	
	#RGB Red, Green, Blue
	screen.fill((0,255,0))

	arena.print(screen)

	if event.type == pygame.KEYUP:
		pressed = False

	player1.print(screen)

	pygame.display.update()