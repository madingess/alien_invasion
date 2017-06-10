class GameStats():
	"""Track statistics for Alien Invasion."""
	
	def __init__(self, game_settings):
		"""Initialize statistics."""
		self.game_settings = game_settings
		self.reset_stats()
		
		# Start Alien Invasion in an inactive state.
		self.game_active = False
		
		# High score should never be reset.
		self.hs_file = 'high_score.txt'
		self.high_score = self.read_high_score()
		
	def read_high_score(self):
		"""Initialize the high score on startup."""
		with open(self.hs_file, 'r') as file_object:
			return int(file_object.read())
		
	def write_high_score(self, score):
		"""Write the current high score to file."""
		with open(self.hs_file, 'w') as file_object:
			file_object.write(str(score))
				
	def reset_stats(self):
		"""Initialize statistics that can change during the game."""
		self.ships_left = self.game_settings.ship_limit
		self.score = 0
		self.level = 1
