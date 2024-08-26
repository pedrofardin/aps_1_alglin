import pygame
import sys
import os
from angry_birds.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class GameOverScreen:
    def __init__(self, screen):
        background_image_path = os.path.join(os.path.dirname(__file__), 'background.png')
        game_over_image_path = os.path.join(os.path.dirname(__file__), 'game_over.png')

        self.screen = screen
        self.background_image = pygame.transform.scale(pygame.image.load(background_image_path), (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.game_over_image = pygame.image.load(game_over_image_path)


    def display(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.blit(self.background_image, (0, 0))

            self.screen.blit(self.game_over_image, (SCREEN_WIDTH // 1.9 - self.game_over_image.get_width() // 2, -10))

            pygame.display.flip()