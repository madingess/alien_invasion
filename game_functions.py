import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien
from random import choice

def get_number_aliens_x(game_settings, alien_width):
	"""Determine the number of aliens that fin in a row."""
	available_space_x = game_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x
	
def get_number_rows(game_settings, ship_height, alien_height):
	"""Determine the number of rows of aliens that fit on the screen."""
	available_space_y = (game_settings.screen_height - 
							(3 * alien_height) - ship_height)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows
		
def create_alien(game_settings, screen, aliens, alien_number, row_number):
	"""Create an alien and place it in the row."""
	alien = Alien(game_settings, screen)
	alien.x = alien.rect.width + 2 * alien.rect.width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)
	
def create_fleet(game_settings, screen, ship, aliens):
	"""Create a full fleet of aliens."""
	# Create an alien and find the number of aliens in a row
	alien = Alien(game_settings, screen)
	number_aliens_x = get_number_aliens_x(game_settings, alien.rect.width)
	number_rows = get_number_rows(game_settings, ship.rect.height,
		alien.rect.height)
	
	# Create the first row of aliens.
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(game_settings, screen, aliens, alien_number,
				row_number)
				
def change_fleet_direction(game_settings, aliens):
	"""Drop the entire fleet and change the fleet's direction."""
	for alien in aliens.sprites():
		alien.rect.y += game_settings.fleet_drop_speed
	game_settings.fleet_direction *= -1			
				
def check_fleet_edges(game_settings, aliens):
	"""Respond appropriately if any aliens have reached an edge."""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(game_settings, aliens)
			break

def check_keydown_events(event, game_settings, screen, stats, sb, ship, 
	aliens, bullets):
	"""Respond to keypresses."""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(game_settings, screen, ship, bullets)
	elif event.key == pygame.K_q:
		stats.write_high_score(stats.high_score)
		sys.exit()
	elif event.key == pygame.K_s and not stats.game_active:
		start_game(game_settings, screen, stats, sb, ship, aliens, bullets)
	elif event.key == pygame.K_p:
		if stats.game_pause == True:
			stats.game_pause = False
		else:
			stats.game_pause = True
	elif event.key == pygame.K_r:
		stats.game_active = False
		pygame.mouse.set_visible(True)
	elif event.key == pygame.K_e:
		stats.game_settings.toggle_easy_mode()

def check_keyup_events(event, ship):
	"""Respond to key releases."""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False
		
def check_events(game_settings, screen, stats, sb, play_button, ship, aliens, 
	bullets):
	"""Respond to keypresses and mouse events."""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, game_settings, screen, stats, 
				sb, ship, aliens, bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(game_settings, screen, stats, sb, 
				play_button, ship, aliens, bullets, mouse_x, mouse_y)
			
def check_play_button(game_settings, screen, stats, sb, play_button, ship, aliens, 
	bullets, mouse_x, mouse_y):
	"""Start a new game when the player clicks Play."""
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		start_game(game_settings, screen, stats, sb, ship, aliens, bullets)
		
def start_game(game_settings, screen, stats, sb, ship, aliens, bullets):
	"""Start a new game."""
	# Unpause if paused
	stats.game_pause = False
	# Reset the game settings.
	game_settings.initialize_dynamic_settings()
	# Hide the mouse cursor.
	pygame.mouse.set_visible(False)
	# Reset the game statistics.
	stats.reset_stats()
	stats.game_active = True
	# Reset the scoreboard images.
	sb.prep_images()
	# Empty the list of aliens and bullets.
	aliens.empty()
	bullets.empty()
	# Create a new fleet and center the ship.
	create_fleet(game_settings, screen, ship, aliens)
	ship.center_ship()
	
def start_new_level(game_settings, screen, stats, sb, ship, aliens,
		bullets):
	"""Start a new level."""
	bullets.empty()
	game_settings.increase_speed()
	create_fleet(game_settings, screen, ship, aliens)
	# Increase level.
	stats.level += 1
	sb.prep_level()
			
def fire_bullet(game_settings, screen, ship, bullets):
	"""Fire a bullet if limit not reached yet."""
	# Create a bullet and add it to the bullets group.
	if len(bullets) < game_settings.bullets_allowed:
		new_bullet = Bullet(game_settings, screen, ship)
		bullets.add(new_bullet)
		sound_bullet_fired(game_settings)
		
def update_screen(game_settings, screen, backdrop, stats, sb, ship, aliens, bullets, 
	play_button):
	"""Update images on the screen and flip to the new screen."""
	# Redraw the screen during each pass through the loop
	backdrop.blitme()
	# Redraw all bullets behind ship and aliens.
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)
	# Draw the score information
	sb.show_score()
	# Draw the play button if the game is inactive.
	if not stats.game_active:
		play_button.draw_button()
			
	# Make the most recently drawn screen visible.
	pygame.display.flip()

def update_bullets(game_settings, screen, stats, sb, ship, aliens, bullets):
	"""Update the position of bullets and get rid of old bullets."""
	bullets.update()
	# Remove bullets that hit the top
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	check_bullet_alien_collisions(game_settings, screen, stats, sb, 
		ship, aliens, bullets)
		
def check_high_score(stats, sb):
	"""Check to see if there's a new high score."""
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()	
	
def check_bullet_alien_collisions(game_settings, screen, stats, sb, 
	ship, aliens, bullets):
	"""Respond to bullet-alien collisions."""
	collisions = pygame.sprite.groupcollide(bullets, aliens, 
		game_settings.bullet_phase, True)
	if collisions:
		for aliens in collisions.values():
			stats.score += game_settings.alien_points * len(aliens)
			sb.prep_score()
		check_high_score(stats, sb)
		sound_bullet_hit(game_settings)
	# If the entire fleet is destroyed, start a new level.
	if len(aliens) == 0:
		start_new_level(game_settings, screen, stats, sb, ship, aliens,
			bullets)

def ship_hit(game_settings, stats, screen, sb, ship, aliens, bullets):
	"""Respond to ship being hit by alien."""
	# Decrement ships left.
	if stats.ships_left > 1:
		stats.ships_left -= 1
		# Update Scoreboard.
		sb.prep_ships()
		# Empty the list of aliens and bullets.
		aliens.empty()
		bullets.empty()
		# Create a new fleet and center the ship.
		create_fleet(game_settings, screen, ship, aliens)
		ship.center_ship()
		sleep(0.5)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)
	
def check_aliens_bottom(game_settings, stats, screen, sb, ship, aliens, bullets):
	"""Check if any aliens have reached the bottome of the screen."""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			# Treat this the same as if the ship got hit.
			ship_hit(game_settings, stats, screen, sb, ship, aliens, bullets)
			break

def update_aliens(game_settings, stats, screen, sb, ship, aliens, bullets):
	"""
	Check if the fleet is at an edge,
	 and update the positions of all aliens in the fleet.
	"""
	check_fleet_edges(game_settings, aliens)
	aliens.update()
	
	# Look for alien-ship collisions.
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(game_settings, stats, screen, sb, ship, aliens, bullets)
	# Look for aliens at the bottom of the screen.
	check_aliens_bottom(game_settings, stats, screen, sb, ship, aliens, bullets)

def sound_bullet_hit(game_settings):
	"""Select and play alien hit soundfile."""
	soundfile = choice(game_settings.bullet_hit_sounds)
	pygame.mixer.Sound(soundfile)
 
def sound_bullet_fired(game_settings):
	"""Select and play bullet fired soundfile."""
	soundfile = choice(game_settings.bullet_fire_sounds)
	pygame.mixer.Sound(soundfile)
