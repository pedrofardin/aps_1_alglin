import pygame
import sys
from angry_birds.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class GameOverScreen:
    def __init__(self, screen):
        self.screen = screen
        self.background_image = pygame.transform.scale(pygame.image.load("angry_birds/images/background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.game_over_image = pygame.image.load("angry_birds/images/game_over.png")


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