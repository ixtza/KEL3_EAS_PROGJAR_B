import threading
from game import Game

if __name__ == "__main__":
	g = Game()
	g.game_loop()
	# threading.Thread(target=g.game_loop()).start()
	# while g.running:
