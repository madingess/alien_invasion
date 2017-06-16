import pygame	# For game funcionalities
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from ship import Ship
from button import Button
from scoreboard import Scoreboard
from backdrop import Backdrop
import game_functions as gf

def run_game():
	# Initialize game and create a screen object
	pygame.init()
	game_settings = Settings()
	screen = pygame.display.set_mode(
		(game_settings.screen_width, game_settings.screen_height))
	pygame.display.set_caption("Alien Invasion")
	backdrop = Backdrop(screen)
	
	# Make the Play button.
	play_button = Button(game_settings, screen, "Play")
	
	# Create an instance to store game statistics and make a scoreboard.
	stats = GameStats(game_settings)
	sb = Scoreboard(game_settings, screen, stats)
	
	# Make a ship, a group of bullets, and a group of aliens.
	ship = Ship(game_settings, screen)
	bullets = [Group(), Group()]
	  #First group for player bullets, second for alien bullets
	aliens = Group()
	
	# Create the fleet of aliens.
	gf.create_fleet(game_settings, screen, ship, aliens)
	
	# Start the main loop for the game.
	while True:
		gf.check_events(game_settings, screen, stats, sb, play_button, 
			ship, aliens, bullets)
		
		if stats.game_active and not stats.game_pause:
			ship.update()
			gf.update_bullets(game_settings, screen, stats, sb, ship,
				aliens, bullets)
			gf.update_aliens(game_settings, stats, screen, sb, ship, 
				aliens, bullets)

		gf.update_screen(game_settings, screen, backdrop, stats, sb, ship, aliens, 
			bullets, play_button)
		
run_game()
