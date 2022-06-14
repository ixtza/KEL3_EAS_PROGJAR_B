import pygame
import random
import Break
import Energy
import Loss
import WarningBreak
import WarningLoss
import os

from frontend.WarningBreak import WarningBreak

#working directory path
work_dir = os.path.dirname(os.path.realpath(__file__))


class Arena:
	#energys and breaks
	illegal_place = [(5, 5)]
	breaks = []
	energys = []
	loss = []
	warning_breaks = []
	warning_loss = []
	
	num_of_breaks = 12
	num_of_energys = 12
	num_of_loss = 12
	num_of_warning_breaks = 48
	num_of_warning_loss = 48

	def __init__(self, img, x, y):
		self.img = img
		self.x = x
		self.y = y

	def print(self, screen):
		screen.blit(self.img, (self.x, self.y))

		for i in range(self.num_of_breaks):
			self.breaks[i].print(screen)

		for i in range(self.num_of_energys):
			self.energys[i].print(screen)
		
		for i in range(self.num_of_loss):
			self.loss[i].print(screen)
		
		for i in range(self.num_of_warning_breaks):
			self.warning_breaks[i].print(screen)
		
		for i in range(self.num_of_warning_loss):
			self.warning_loss[i].print(screen)

	#generate energy and brekas
	def generate_map(self):
		for i in range(self.num_of_energys):
			randX = 5
			randY = 5
			while (randX, randY) in self.illegal_place:
				if i < 3:
					randX = random.randint(1, 5)
					randY = random.randint(1, 5)
				elif i < 6:
					randX = random.randint(5, 9)
					randY = random.randint(1, 5)
				elif i < 9:
					randX = random.randint(1, 5)
					randY = random.randint(5, 9)
				elif i < 12:
					randX = random.randint(5, 9)
					randY = random.randint(5, 9)
			self.energys.append(Energy.Energy(pygame.image.load(
				work_dir + "/assets/energy/energy.png"), randX * 32, randY * 32))
			self.illegal_place.append((randX, randY))

		for i in range(self.num_of_breaks):
			randX = 5
			randY = 5
			while (randX, randY) in self.illegal_place:
				if i < 3:
					randX = random.randint(1, 5)
					randY = random.randint(1, 5)
				elif i < 6:
					randX = random.randint(5, 9)
					randY = random.randint(1, 5)
				elif i < 9:
					randX = random.randint(1, 5)
					randY = random.randint(5, 9)
				elif i < 12:
					randX = random.randint(5, 9)
					randY = random.randint(5, 9)
			self.breaks.append(Break.Break(pygame.image.load(
				work_dir + "/assets/break/break.png"), randX * 32, randY * 32))
			self.warning_breaks.append(WarningBreak.WarningBreak(pygame.image.load(
				work_dir + "/assets/warning_break/warning_break.png"), (randX + 1) * 32, (randY) * 32))
			self.warning_breaks.append(WarningBreak.WarningBreak(pygame.image.load(
				work_dir + "/assets/warning_break/warning_break.png"), (randX) * 32, (randY + 1) * 32))
			self.warning_breaks.append(WarningBreak.WarningBreak(pygame.image.load(
				work_dir + "/assets/warning_break/warning_break.png"), (randX - 1) * 32, (randY) * 32))
			self.warning_breaks.append(WarningBreak.WarningBreak(pygame.image.load(
				work_dir + "/assets/warning_break/warning_break.png"), (randX) * 32, (randY - 1) * 32))
			self.illegal_place.append((randX, randY))

		for i in range(self.num_of_loss):
			randX = 5
			randY = 5
			while (randX, randY) in self.illegal_place:
				if i < 3:
					randX = random.randint(1, 5)
					randY = random.randint(1, 5)
				elif i < 6:
					randX = random.randint(5, 9)
					randY = random.randint(1, 5)
				elif i < 9:
					randX = random.randint(1, 5)
					randY = random.randint(5, 9)
				elif i < 12:
					randX = random.randint(5, 9)
					randY = random.randint(5, 9)
			self.loss.append(Loss.Loss(pygame.image.load(
				work_dir + "/assets/loss/loss.png"), randX * 32, randY * 32))
			self.warning_loss.append(WarningLoss.WarningLoss(pygame.image.load(
				work_dir + "/assets/warning_loss/warning_loss.png"), (randX + 1) * 32, (randY) * 32))
			self.warning_loss.append(WarningLoss.WarningLoss(pygame.image.load(
				work_dir + "/assets/warning_loss/warning_loss.png"), (randX) * 32, (randY + 1) * 32))
			self.warning_loss.append(WarningLoss.WarningLoss(pygame.image.load(
				work_dir + "/assets/warning_loss/warning_loss.png"), (randX - 1) * 32, (randY) * 32))
			self.warning_loss.append(WarningLoss.WarningLoss(pygame.image.load(
				work_dir + "/assets/warning_loss/warning_loss.png"), (randX) * 32, (randY - 1) * 32))
			self.illegal_place.append((randX, randY))

	def getBreaks(self):
		return self.breaks

	def getEnergys(self):
		return self.energys

	def getLoss(self):
		return self.loss
	
	def getWarningBreaks(self):
		return self.warning_breaks
	
	def getWarningLoss(self):
		return self.warning_loss