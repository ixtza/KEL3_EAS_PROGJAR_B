import pygame, os , time

# Title state
from states.title import Title

class Game():
	def __init__(self):
		pygame.init()

		self.GAME_W,self.GAME_H = 528, 416
		self.SCREEN_W,self.SCREEN_H = 800, 600
		self.game_canvas = pygame.Surface((self.GAME_W,self.GAME_H))
		self.display = pygame.display.set_mode((self.SCREEN_W,self.SCREEN_H))
		self.running, self.playing = True, True
		self.actions = {
			"keydown": False, 
			"keyup": True,
			"left": False, 
			"right": False, 
			"up" : False, 
			"down" : False, 
			"action1" : False, 
			"action2" : False, 
			"start" : False
			}
		self.state_stack = []
		self.BLACK, self.WHITE = (0,0,0),(255,255,255)

		# game ticks
		self.dt, self.prev_time = 0, 0

		# load assets
		self.load_assets()

		# load states
		self.load_states()

	def game_loop(self):
		while self.playing:
			self.get_dt()
			self.get_events()
			self.render()
			self.update()

	def get_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.playing = False
				self.running = False
			if event.type == pygame.KEYDOWN:
				self.actions['keyup'] = False
				self.actions['keydown'] = True
				if event.key == pygame.K_ESCAPE:
					self.playing = False
					self.running = False
				if event.key == pygame.K_LEFT:
					self.actions['left'] = True
				if event.key == pygame.K_RIGHT:
					self.actions['right'] = True
				if event.key == pygame.K_UP:
					self.actions['up'] = True
				if event.key == pygame.K_DOWN:
					self.actions['down'] = True
				if event.key == pygame.K_p:
					self.actions['action1'] = True
				if event.key == pygame.K_o:
					self.actions['action2'] = True    
				if event.key == pygame.K_RETURN:
					self.actions['start'] = True  

			if event.type == pygame.KEYUP:
				self.actions['keydown'] = False
				self.actions['keyup'] = True
				if event.key == pygame.K_LEFT:
					self.actions['left'] = False
				if event.key == pygame.K_RIGHT:
					self.actions['right'] = False
				if event.key == pygame.K_UP:
					self.actions['up'] = False
				if event.key == pygame.K_DOWN:
					self.actions['down'] = False
				if event.key == pygame.K_p:
					self.actions['action1'] = False
				if event.key == pygame.K_o:
					self.actions['action2'] = False
				if event.key == pygame.K_RETURN:
					self.actions['start'] = False
	
	def update(self):
		self.state_stack[-1].update(self.dt,self.actions)
		pass

	def render(self):
		self.state_stack[-1].render(self.game_canvas)
		# Render current state to the screen
		self.display.blit(pygame.transform.scale(self.game_canvas,(self.SCREEN_W, self.SCREEN_H)), (0,0))
		pygame.display.flip()

	def get_dt(self):
		now = time.time()
		self.dt = now - self.prev_time
		self.prev_time = now

	def draw_text(self, surface, text, color, x, y):
		text_surface = self.font.render(text, True, color)
		#text_surface.set_colorkey((0,0,0))
		text_rect = text_surface.get_rect()
		text_rect.center = (x, y)
		surface.blit(text_surface, text_rect)

	def load_assets(self):
		# Create pointers to directories 
		self.work_dir = os.path.dirname(os.path.realpath(__file__))
		self.assets_dir = os.path.join(self.work_dir,"assets")
		self.player_dir = os.path.join(self.assets_dir, "player")
		self.font_dir = os.path.join(self.assets_dir, "font")
		self.font= pygame.font.Font(os.path.join(self.font_dir, "PressStart2P-vaV7.ttf"), 20)
		pass

	def load_states(self):
		self.title_screen = Title(self)
		self.state_stack.append(self.title_screen)

	def reset_keys(self):
		for action in self.actions:
			self.actions[action] = False