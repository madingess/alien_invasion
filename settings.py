class Settings():
	"""A class to store all settings for Alien Invasion."""
	
	def __init__(self):
		"""Initialize the game's static settings."""
		# Screen settings
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (230, 230, 230)
		
		# Ship settings
		self.ship_limit = 3
		
		# Bullet settings
		self.bullet_height = 15
		self.bullet_color = 60, 60, 60
		self.bullets_allowed = 3

		# Alien Settings
		self.fleet_drop_speed = 10

		# Game speed scaling per level increase
		self.speedup_scale = 1.1
		# Alien point value scaling per level increase
		self.score_scale = 1.5
		
		self.initialize_dynamic_settings()
		
	def initialize_dynamic_settings(self):
		"""Initialize settings that change throughout the game."""
		self.ship_speed_factor = 1.5
		self.bullet_speed_factor = 3
		self.alien_speed_factor = 1
		
		self.fleet_direction = 1  # (1) means right  (-1) means left
		
		# Scoring
		self.alien_points = 50
		
		# Easy mode settings
		self.easy_mode = False
		self.bullet_width = 3
		self.bullet_phase = True  # True means bullets disappear on hits

	def increase_speed(self):
		"""Increase speed settings and alien point values."""
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
		
		self.alien_points = int(self.alien_points * self.score_scale)

	def toggle_easy_mode(self):
		"""Toggle easy mode on/off."""
		if self.easy_mode:
			self.bullet_width = 3
			self.bullet_phase = True
			self.easy_mode = False
		else:
			self.bullet_width = 300
			self.bullet_phase = False
			self.easy_mode = True
		
