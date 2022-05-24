import pygame
import random
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
arenaImg = pygame.image.load(work_dir+"/assets/arena/arena.png")
arenaX = 0
arenaY = 0

def Arena(x,y):
	screen.blit(arenaImg,(x,y))

#players
player1Img = pygame.image.load(work_dir+"/assets/player/player1.png")
player1X = 0
player1Y = 320

def Player1(x,y):
	screen.blit(player1Img,(x,y))

#keyboard
pressed = False

#energys and breaks
illegal_place = [(5,5)]

#break
breakImg = []
breakX = []
breakY = []
num_of_breaks = 12

for i in range(num_of_breaks):
	breakImg.append(pygame.image.load(work_dir+"/assets/break/break.png"))
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
	breakX.append(32*randX)
	breakY.append(32*randY)
	illegal_place.append((randX,randY))

def Break(x,y,i):
	screen.blit(breakImg[i],(x,y))

#energy
energyImg = []
energyX = []
energyY = []
num_of_energys = 12

for i in range(num_of_energys):
	energyImg.append(pygame.image.load(work_dir+"/assets/energy/energy.png"))
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
	energyX.append(32*randX)
	energyY.append(32*randY)
	illegal_place.append((randX,randY))

def Break(x,y,i):
	screen.blit(breakImg[i],(x,y))

def Energy(x,y,i):
	screen.blit(energyImg[i],(x,y))

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
			player1X = player1X - 32
		if event.key == pygame.K_RIGHT:
			player1X = player1X + 32
		if event.key == pygame.K_UP:
			player1Y = player1Y - 32
		if event.key == pygame.K_DOWN:
			player1Y = player1Y + 32

	if player1X < 0:
		player1X = 0
	if player1X > 352:
		player1X = 352
	if player1Y < 0:
		player1Y = 352
	if player1Y > 352:
		player1Y = 352

	if event.type == pygame.KEYUP:
		pressed = False

	Player1(player1X,player1Y)

	for i in range(num_of_breaks):
		Break(breakX[i], breakY[i], i)
	
	for i in range(num_of_energys):
		Energy(energyX[i], energyY[i], i)

	pygame.display.update()