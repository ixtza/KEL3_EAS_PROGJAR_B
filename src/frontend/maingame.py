from re import L
import pygame

#importing game classes
import Player
import Arena
import GameController
import Text

import random
import os
import time

#clear console
def clear_console():
    os.system('cls')

#working directory path
work_dir = os.path.dirname(os.path.realpath(__file__))

#initialize the pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((352, 486))

#title and icon
pygame.display.set_caption("Tap Treasure")
icon = pygame.image.load(work_dir + "/assets/icon/treasure.png")
pygame.display.set_icon(icon)

#arena
arena = Arena.Arena(pygame.image.load(
    work_dir + "/assets/arena/arena.png"), 0, 0)
arena.generate_map()

#players
players = []
players.append(Player.Player(pygame.image.load(
    work_dir+"/assets/model/model_move.png").convert_alpha(), 0, 0, 320))
players.append(Player.Player(pygame.image.load(
    work_dir+"/assets/model/model_move.png").convert_alpha(), 1, 0, 0))
players.append(Player.Player(pygame.image.load(
    work_dir+"/assets/model/model_move.png").convert_alpha(), 2, 320, 0))
players.append(Player.Player(pygame.image.load(
    work_dir+"/assets/model/model_move.png").convert_alpha(), 3, 320, 320))

#text
text = Text.Text(work_dir+"/assets/fonts/ROCK.TTF", 14)

#gamecontroller
gamecontroller = GameController.GameController(0)

#game ticks
dt = 0
prevTime = 0
clock = pygame.time.Clock()


def get_dt(lastUpdate):
	now = time.time()
	dt = now - lastUpdate
	prevTime = now
	return dt


#gameloop
running = True
while running:
	clock.tick(60)
	for event in pygame.event.get():
		dt = get_dt(prevTime)
		if event.type == pygame.QUIT:
			running = False

		#Check input for specific player
		player = players[gamecontroller.getturn()]
		changeTurn = player.check_movement(event)
		#If any valid input from player
		if changeTurn:
			if player.point >= 0:
				player.setPoint(player.getPoint() - 1)

			clear_console()
			print("Current score status: "
                            + str(players[0].getPoint()) + " "
                            + str(players[1].getPoint()) + " "
                            + str(players[2].getPoint()) + " "
                            + str(players[3].getPoint())
         )

			#check for break, energy, and finish
			for brk in arena.getBreaks():
				if player.getX() == brk.getX() and player.getY() == brk.getY():
					gamecontroller.addEliminated(gamecontroller.getturn())
			for energy in arena.getEnergys():
				if player.getX() == energy.getX() and player.getY() == energy.getY():
					point = 6
					player.setPoint(player.getPoint() + point)
					print("Player " + str(player.id + 1) + " get " + str(point) + " points.")
			for loss in arena.getLoss():
				if player.getX() == loss.getX() and player.getY() == loss.getY():
					point = -4
					player.setPoint(player.getPoint() + point)
					print("Player " + str(player.id + 1) + " get " + str(point) + " loss.")
			for warning_break in arena.getWarningBreaks():
				if player.getX() == warning_break.getX() and player.getY() == warning_break.getY():
					print("Warning for Player " + str(player.id + 1) + "! there is a break near you.")
			for warning_loss in arena.getWarningLoss():
				if player.getX() == warning_loss.getX() and player.getY() == warning_loss.getY():
					print("Warning for Player " + str(player.id + 1) + "! there is a loss near you.")
			if player.getX() == 160 and player.getY() == 160:
				gamecontroller.addEliminated(gamecontroller.getturn())

			if player.point <= 0:
				gamecontroller.addRunOutOfPoints(gamecontroller.getturn())

			#check if all players is finished
			if (len(gamecontroller.getEliminated()) > 3):
				maxpoint = -999999
				winner = 0
				for player in players:
					if player.getPoint() > maxpoint:
						maxpoint = player.getPoint()
						winner = player.getId()+1
				print("Player " + str(winner) + " Win!")
				running = False

			gamecontroller.nextturn()

	#RGB Red, Green, Blue
	screen.fill((255, 255, 255))

	arena.print(screen)

	Ytext = 410
	for player in players:
		Ytext += 15
		player.update(dt)
		player.render(screen)
		text.print(screen, "Player " + str(player.getId()) + " Score :" + str(player.getPoint()), 64, Ytext)

	text.print(screen, "Player " + str(gamecontroller.getturn() + 1) + "'s Turn", 260, 430)
	pygame.display.update()