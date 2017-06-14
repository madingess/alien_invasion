import pygame

class Backdrop():
	"""Sprite to blit the backround image onto the screen"""
	
	def __init__(self, screen):
		"""Initialize the backdrop to it's static position."""
		self.screen = screen
		
		# Initialize image and rectangle
		self.image = pygame.image.load('images/backdrop.bmp').convert()
		self.rect = self.image.get_rect()
		self.screen_rect = self.screen.get_rect()
		
		# Initialize positions
		self.rect.centerx = self.screen_rect.centerx
		self.rect.centery = self.screen_rect.centery
		
	def blitme(self):
		self.screen.blit(self.image, self.rect)
