import pygame
import sys
import os
from angry_birds.bird import Bird
from angry_birds.moon import Moon
from angry_birds.force_visualizer import ForceVisualizer
from angry_birds.constants import *
from angry_birds.button import Button
from angry_birds.home import HomeScreen
from angry_birds.game_over import GameOverScreen
from angry_birds.about import AboutScreen

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Angry Birds")

base_path = os.path.dirname(__file__)

# Use pkg_resources to load images from the package
player_bird_images = [
    pygame.transform.scale(pygame.image.load(os.path.join(base_path,'pimages/layer_bird.png')), (75, 75)),
    pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'images/red_bird.png')), (75, 75))
]
pig_image = pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'images/enemy_bird.png')), (50, 50))

slingshot_image = pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'images/estilingue.png')), (100, 100))

background_image = pygame.image.load(os.path.join(base_path, 'images/background.png'))
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

player_bird = Bird(SCREEN_WIDTH // 5, SCREEN_HEIGHT * 4 // 5, player_bird_images)

refresh_button = Button(10, 10, pygame.image.load(os.path.join(base_path, 'images/refresh_button.png')), "refresh")


moon_positions = [
    (SCREEN_WIDTH * 0.35, SCREEN_HEIGHT * 0.25),
    (SCREEN_WIDTH * 0.75, SCREEN_HEIGHT * 0.25),
    (SCREEN_WIDTH * 0.55, SCREEN_HEIGHT * 0.5),
    (SCREEN_WIDTH * 0.75, SCREEN_HEIGHT * 0.75),
    (SCREEN_WIDTH * 0.35, SCREEN_HEIGHT * 0.75)
]

pig_positions = [
    (SCREEN_WIDTH * 0.55, SCREEN_HEIGHT * 0.25),
    (SCREEN_WIDTH * 0.75, SCREEN_HEIGHT * 0.5),
    (SCREEN_WIDTH * 0.35, SCREEN_HEIGHT * 0.5),
    (SCREEN_WIDTH * 0.55, SCREEN_HEIGHT * 0.75),
    (SCREEN_WIDTH * 0.85, SCREEN_HEIGHT * 0.75),
    (SCREEN_WIDTH * 0.85, SCREEN_HEIGHT * 0.5),
    (SCREEN_WIDTH * 0.85, SCREEN_HEIGHT * 0.25),
    (SCREEN_WIDTH * 0.93, SCREEN_HEIGHT * 0.25),
    (SCREEN_WIDTH * 0.93, SCREEN_HEIGHT * 0.5),
    (SCREEN_WIDTH * 0.93, SCREEN_HEIGHT * 0.75)
]

moons = [Moon(x, y) for x, y in moon_positions]

pigs = pygame.sprite.Group()
for pos in pig_positions:
    pig = Bird(pos[0], pos[1], pig_image)
    pigs.add(pig)

force_visualizer = ForceVisualizer(screen, player_bird)

score = 0

def main():
    clock = pygame.time.Clock()
    home_screen = HomeScreen(screen)
    about_screen = AboutScreen(screen)
    game_over_screen = GameOverScreen(screen)
    game_state = "home_screen"

    while True:
        if game_state == "home_screen":
            home_screen.draw()
            game_state = home_screen.handle_events()
        elif game_state == "game_over":
            game_over_screen.display()
            game_state = "home_screen"  # Reset to home screen after game over
        elif game_state == "start_game":
            game_state = run_game()  # Update game_state based on the result of run_game()
        elif game_state == "about_screen":
            running = about_screen.handle_events()
            if not running:
                game_state = "home_screen"
            else:
                about_screen.draw()
        clock.tick(60)

def run_game():
    global score, player_bird, pigs

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if refresh_button.rect.collidepoint(event.pos):
                    # Reset the game; reposition the birds and the pigs
                    player_bird.rect.center = (SCREEN_WIDTH // 5, SCREEN_HEIGHT * 4 // 5)
                    player_bird.velocity = [0, 0]
                    player_bird.not_released = True
                    pigs.empty()
                    for pos in pig_positions:
                        pig = Bird(pos[0], pos[1], pig_image)
                        pigs.add(pig)
                    score = 0

                elif player_bird.rect.collidepoint(event.pos):
                    player_bird.start_drag() 

            elif event.type == pygame.MOUSEBUTTONUP:
                if player_bird.dragging:
                    player_bird.end_drag()

        if not player_bird.not_released:  # Apply gravity to the bird if it was released
            player_bird.velocity[1] += player_bird.gravity / 10
        
        for moon in moons:
            moon.apply_gravity(player_bird)
            moon.handle_collision(player_bird)  # Check collision with the moon

        # Bird animation
        if player_bird.dragging or not player_bird.not_released:
            player_bird.current_frame = 0
        else:
            player_bird.current_frame = 1

        # Check collision with pigs
        hits = pygame.sprite.spritecollide(player_bird, pigs, True)
        if hits:
            for hit_enemy in hits:
                score = hit_enemy.hit_enemy(score)

        if len(pigs) == 0:
            return "game_over"  # End the game when all pigs are gone

        # Check if the bird is out of bounds
        if player_bird.rect.left > SCREEN_WIDTH or player_bird.rect.right < 0 or \
                player_bird.rect.top > SCREEN_HEIGHT or player_bird.rect.bottom < -200:
            player_bird.rect.center = (SCREEN_WIDTH // 5, SCREEN_HEIGHT * 4 // 5)
            player_bird.velocity = [0, 0]
            player_bird.not_released = True

        # Drawing section
        screen.blit(background_image, (0, 0))
        
        for moon in moons:
            screen.blit(moon.image, moon.rect)

        screen.blit(slingshot_image, (SCREEN_WIDTH // 5 - 20, SCREEN_HEIGHT - 100))
        player_bird.update()
        screen.blit(player_bird.image, player_bird.rect)

        for pig in pigs:
            pig.update()
            screen.blit(pig.image, pig.rect)

        screen.blit(refresh_button.image, refresh_button.rect)
        
        force_visualizer.visualize_forces()

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Pontuação: {score}", True, (255, 0, 0))
        screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 10, 10))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
