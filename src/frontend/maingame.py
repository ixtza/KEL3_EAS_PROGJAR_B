from pickle import FALSE
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
screen = pygame.display.set_mode((352, 531)) # prev 352, 486

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

#marker
marker_GotPoints = False
marker_GotBreak = False
marker_GotLoss = False
marker_NearBreak = False
marker_NearLoss = False
marker_RunOutOfPoints = False
marker_Wins = False

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
			marker_GotPoints = False
			marker_GotBreak = False
			marker_GotLoss = False
			marker_NearBreak = False
			marker_NearLoss = False
			marker_RunOutOfPoints = False
			savePlayerId_GotPoints = 0
			savePlayerId_GotBreak = 0
			savePlayerId_GotLoss = 0
			savePlayerId_NearBreak = 0
			savePlayerId_NearLoss = 0
			savePlayerId_RunOutOfPoints = 0
			savePlayerId_Wins = 0

			for brk in arena.getBreaks():
				if player.getX() == brk.getX() and player.getY() == brk.getY():
					gamecontroller.addEliminated(gamecontroller.getturn())
					savePlayerId_GotBreak = player.id + 1
					marker_GotBreak = True
				if player.getX() == brk.getX() - 32 and player.getY() == brk.getY() - 32:
					print("There's a break near Player " + str(player.id + 1) + "!")
					savePlayerId_NearBreak = player.id + 1
					marker_NearBreak = True
				if player.getX() == brk.getX() - 32 and player.getY() == brk.getY() + 32:
					print("There's a break near Player " + str(player.id + 1) + "!")
					savePlayerId_NearBreak = player.id + 1
					marker_NearBreak = True
				if player.getX() == brk.getX() + 32 and player.getY() == brk.getY() - 32:
					print("There's a break near Player " + str(player.id + 1) + "!")
					savePlayerId_NearBreak = player.id + 1
					marker_NearBreak = True
				if player.getX() == brk.getX() + 32 and player.getY() == brk.getY() + 32:
					print("There's a break near Player " + str(player.id + 1) + "!")
					savePlayerId_NearBreak = player.id + 1
					marker_NearBreak = True
			for energy in arena.getEnergys():
				if player.getX() == energy.getX() and player.getY() == energy.getY():
					point = 8
					player.setPoint(player.getPoint() + point)
					print("Player " + str(player.id + 1) + " get " + str(point) + " points.")
					savePlayerId_GotPoints = player.id + 1
					marker_GotPoints = True
			for loss in arena.getLoss():
				if player.getX() == loss.getX() and player.getY() == loss.getY():
					point = -3
					player.setPoint(player.getPoint() + point)
					print("Player " + str(player.id + 1) + " get " + str(point) + " loss.")
					savePlayerId_GotLoss = player.id + 1
					marker_GotLoss = True
				if player.getX() == loss.getX() - 32 and player.getY() == loss.getY():
					print("There's a loss near Player " + str(player.id + 1) + "!")
					savePlayerId_NearLoss = player.id + 1
					marker_NearLoss = True
				if player.getX() == loss.getX() and player.getY() == loss.getY() + 32:
					print("There's a loss near Player " + str(player.id + 1) + "!")
					savePlayerId_NearLoss = player.id + 1
					marker_NearLoss = True
				if player.getX() == loss.getX() + 32 and player.getY() == loss.getY():
					print("There's a loss near Player " + str(player.id + 1) + "!")
					savePlayerId_NearLoss = player.id + 1
					marker_NearLoss = True
				if player.getX() == loss.getX() and player.getY() == loss.getY() - 32:
					print("There's a loss near Player " + str(player.id + 1) + "!")
					savePlayerId_NearLoss = player.id + 1
					marker_NearLoss = True
			if player.getX() == 160 and player.getY() == 160:
				gamecontroller.addEliminated(gamecontroller.getturn())

			if player.point <= 0:
				gamecontroller.addRunOutOfPoints(gamecontroller.getturn())
				savePlayerId_RunOutOfPoints = player.id + 1
				marker_RunOutOfPoints = True

			#check if all players is finished
			if (len(gamecontroller.getEliminated()) > 3):
				maxpoint = -999999
				winner = 0
				for player in players:
					if player.getPoint() > maxpoint:
						maxpoint = player.getPoint()
						winner = player.getId()+1
				print("Player " + str(winner) + " Win!")
				savePlayerId_Wins = player.id + 1
				marker_Wins = True
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

	text.print(screen, "Player " + str(gamecontroller.getturn() + 1) + "'s Turn", 250, 425)
	
	if marker_GotPoints == True:
		text.print(screen, "Player " + str(savePlayerId_GotPoints) + " get " + str(point) + " points.", 64 + 7, 485)
	if marker_NearBreak == True:
		text.print(screen, "There's a break near Player " + str(savePlayerId_NearBreak) + "!", 250, 440)
	if marker_NearLoss == True:
		text.print(screen, "There's a loss near Player " + str(savePlayerId_NearLoss) + "!", 250, 455)
	if marker_GotBreak == True:
		text.print(screen, "Player " + str(savePlayerId_GotBreak) + " gets a break!", 250, 470)
	if marker_GotLoss == True:
		text.print(screen, "Player " + str(savePlayerId_GotLoss) + " get " + str(point) + " loss.", 64 + 7, 500)
	if marker_RunOutOfPoints == True:
		text.print(screen, "Player " + str(savePlayerId_RunOutOfPoints) + " has run out of points.", 105, 515)
	if marker_Wins == True:
		text.print(screen, "Player " + str(savePlayerId_Wins) + " Win!", 64, 515)

	pygame.display.update()