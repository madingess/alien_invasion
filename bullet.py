import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	"""A class to manage bullets fired from a sprite."""
	
	def __init__(self, game_settings, screen, sprite, directionUp):
		"""Crete a bullet object at the ship's current position."""
		super(Bullet, self).__init__()
		self.screen = screen
		
		# Create a bullet rect at (0, 0) and then set correct pos
		self.rect = pygame.Rect(0, 0, game_settings.bullet_width,
			game_settings.bullet_height)
		self.rect.centerx = sprite.rect.centerx
		self.directionUp = directionUp
		if self.directionUp == True:
			self.rect.top = sprite.rect.top
		else:
			self.rect.bottom = sprite.rect.bottom
		
		# Store the bullet's position as a decimal value
		self.y = float(self.rect.y)
		
		self.color = game_settings.bullet_color
		self.speed_factor = game_settings.bullet_speed_factor

	def update(self):
		"""Move the bullet up the screen."""
		# Update the decimal position of the bullet.
		if self.directionUp == True:
			self.y -= self.speed_factor
		else:
			self.y += self.speed_factor
		# Update the rect position.
		self.rect.y = self.y
		
	def draw_bullet(self):
		"""Draw the bullet to the screen."""
		pygame.draw.rect(self.screen, self.color, self.rect)
