import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien

def get_number_aliens_x(ai_settings, alien_width):
    '''calculate how many aliens per line'''
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x/(2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    '''calculate how many rows of aliens on screen'''
    available_space_y = (ai_settings.screen_height - (3 * alien_height)
        - ship_height)
    number_rows = int(available_space_y/ (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number,row_number):
    '''create an alien and put it into the current line'''
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    '''create a fleet of aliens'''
    #create one alien and calculate how many aliens per line
    #space between aliens is the width of aliens
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
        alien.rect.height)

    #create the aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                row_number)

def check_keydown_events(event,ai_settings,screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)

def fire_bullet(ai_settings, screen, ship, bullets):
    '''fire a bullet if the limit is not reached'''
    #create a new bullet and add it to the bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)


def check_keyup_events(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
    bullets):
    '''respond to mouse and keyboard'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button,
                ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button,
    ship, aliens, bullets, mouse_x, mouse_y):
    '''start new game whrn play button is hit'''
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #initialise game Settings
        ai_settings.initialise_dynamic_settings()

        #hide the symbol
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True

        #reset scorebaord images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        #empty alien and bullet groups
        aliens.empty()
        bullets.empty()

        #create a new group of aliens and set ship to center
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
    play_button):
    '''update images on screen'''
    screen.fill(ai_settings.bg_colour)

    #draw bullet after ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    #if game not active, draw the play button
    if not stats.game_active:
        play_button.draw_button()

    #show new images
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb,ship, aliens, bullets):
    '''update positions of bullets and remove disappeared bullets'''
    #update bullet positions
    bullets.update()

    #delete disappeared bullets
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats,
        sb, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats,
    sb, ship, aliens, bullets):
    '''respond to collisions between bullets and aliens'''
    #check if bullets hit aliens
    #if so, delete bullets and aliens
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        #delete present bullets and create a new fleet of aliens and up the game speed/level
        bullets.empty()
        ai_settings.increase_speed()

        #up level
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)

def check_fleet_edges(ai_settings, aliens):
    '''take actions when aliens are at screen edge'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    '''move alien group down and change their direction'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.alien_drop_factor
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    ''' respind to ships hit by aliens'''
    if stats.ships_left > 0:
        # ships_left minus 1
        stats.ships_left -= 1

        #update ship_score
        sb.prep_ships()

        #empty the alien and bullet group
        aliens.empty()
        bullets.empty()

        #create a new fleet of aliens
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        #pause
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    '''check if any aliens are at screen bottom'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #treat it as if ship hit by alien
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)

def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    '''check if there are aliens at screen edge and
        update positions of all aliens'''
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    #check collisions between aliens and ship
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)

    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)

def check_high_score(stats, sb):
    '''check if there is a new record'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
