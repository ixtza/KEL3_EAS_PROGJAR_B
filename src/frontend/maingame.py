import pygame
import random

#importing game classes
import Player
import Break
import Energy

import os 
import model

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
arenaImg = pygame.image.load(work_dir+"/assets/arena/arena.png")
arenaX = 0
arenaY = 0

def Arena(x,y):
	screen.blit(arenaImg,(x,y))

#players
<<<<<<< HEAD
# player1Img = pygame.image.load(work_dir+"/assets/player/player1.png")
player1Img = pygame.image.load(work_dir+"/assets/model/model_move.png").convert_alpha()
player1X = 0
player1Y = 320

spriteModel = model.SpriteModel(player1Img)
player_animation_list = [[]]
player_animation_movement = 4
player_animation_steps = 7
frame = 0

def Player1(x,y,move):
	screen.blit(player1Img,(x,y))
	move = 32
	if move == pygame.K_LEFT:
		frame = 2
		for s in range(player_animation_steps):
			# screen.blit(player1Img,(x,y))
			screen.blit(player_animation_list[s][frame], (x,y))
	if move == pygame.K_RIGHT:
		frame = 1
		for x in range(player_animation_steps):
			# screen.blit(player1Img,(x,y))
			screen.blit(player_animation_list[s][frame], (x,y))
	if move == pygame.K_UP:
		frame = 3
		for x in range(player_animation_steps):
			# screen.blit(player1Img,(x,y))
			screen.blit(player_animation_list[s][frame], (x,y))
	if move == pygame.K_DOWN:
		frame = 0
		for x in range(player_animation_steps):
			# screen.blit(player1Img,(x,y))
			screen.blit(player_animation_list[s][frame], (x,y))

for x in range(player_animation_steps):
	player_animation_list.append([])
	for y in range(player_animation_movement):
		(player_animation_list[x]).append(spriteModel.get_image(x,y,32,32,10,(0,0,0)))
=======
player1 = Player.Player(pygame.image.load(work_dir+"/assets/player/player1.png"), 0, 320)
>>>>>>> b55d8608244672b722aee57df58df369921af282

#keyboard
pressed = False

#energys and breaks
illegal_place = [(5,5)]

#break
breaks = []
energys = []
num_of_breaks = 12
num_of_energys = 12

for i in range(num_of_breaks):
	randX = 5
	randY = 5
	while (randX,randY) in illegal_place:
		if i < 3:
			randX = random.randint(1,5)
			randY = random.randint(1,5)
		elif i < 6:
			randX = random.randint(5,9)
			randY = random.randint(1,5)
		elif i < 9:
			randX = random.randint(1,5)
			randY = random.randint(5,9)
		elif i < 12:
			randX = random.randint(5,9)
			randY = random.randint(5,9)
	breaks.append(Break.Break(pygame.image.load(work_dir+"/assets/break/break.png"), randX*32, randY*32))
	illegal_place.append((randX,randY))

for i in range(num_of_energys):
	randX = 5
	randY = 5
	while (randX,randY) in illegal_place:
		if i < 3:
			randX = random.randint(1,5)
			randY = random.randint(1,5)
		elif i < 6:
			randX = random.randint(5,9)
			randY = random.randint(1,5)
		elif i < 9:
			randX = random.randint(1,5)
			randY = random.randint(5,9)
		elif i < 12:
			randX = random.randint(5,9)
			randY = random.randint(5,9)
	energys.append(Energy.Energy(pygame.image.load(work_dir+"/assets/energy/energy.png"), randX*32, randY*32))
	illegal_place.append((randX,randY))

#gameloop
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	#RGB Red, Green, Blue
	screen.fill((0,255,0))

	Arena(arenaX,arenaY)
		
	if event.type == pygame.KEYDOWN and pressed == False:
		pressed = True
		if event.key == pygame.K_LEFT:
			player1.x = player1.x - 32
		if event.key == pygame.K_RIGHT:
			player1.x = player1.x + 32
		if event.key == pygame.K_UP:
			player1.y = player1.y - 32
		if event.key == pygame.K_DOWN:
			player1.y = player1.y + 32

<<<<<<< HEAD
	if player1X < 0:
		player1X = 0
	if player1X > 320:
		player1X = 320
	if player1Y < 0:
		player1Y = 0
	if player1Y > 320:
		player1Y = 320
=======
	if player1.x < 0:
		player1.x = 0
	if player1.x > 352:
		player1.x = 352
	if player1.y < 0:
		player1.y = 352
	if player1.y > 352:
		player1.y = 352
>>>>>>> b55d8608244672b722aee57df58df369921af282

	if event.type == pygame.KEYUP:
		pressed = False

<<<<<<< HEAD
	Player1(player1X,player1Y,event.key)
=======
	player1.print(screen)
>>>>>>> b55d8608244672b722aee57df58df369921af282

	for i in range(num_of_breaks):
		breaks[i].print(screen)
	
	for i in range(num_of_energys):
		energys[i].print(screen)

	pygame.display.update()