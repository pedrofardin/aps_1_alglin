import pygame
import sys
import os
from angry_birds.button import Button
from angry_birds.constants import SCREEN_WIDTH, SCREEN_HEIGHT


class HomeScreen:
    def __init__(self, screen):
        background_image_path = os.path.join(os.path.dirname(__file__), 'images/pixelcut-export.png')
        start_button_image_path = os.path.join(os.path.dirname(__file__), 'images/start_button.png')
        about_button_image_path = os.path.join(os.path.dirname(__file__), 'images/about_button.png')

        self.screen = screen
        
        # Load the background image for the home screen
        self.background_image = pygame.transform.scale(pygame.image.load(background_image_path), (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Load button images and calculate their positions to place them next to each other
        start_button_image = pygame.image.load(start_button_image_path)
        about_button_image = pygame.image.load(about_button_image_path)

        button_width = start_button_image.get_width()
        button_height = start_button_image.get_height()

        total_width = 2 * button_width + 20  # 20 pixels of spacing between buttons
        start_button_x = SCREEN_WIDTH // 2 - total_width // 2
        about_button_x = start_button_x + button_width + 20  # Place about button to the right of start button

        button_y = SCREEN_HEIGHT // 2 - button_height // 2

        self.start_button = Button(start_button_x, button_y, start_button_image, "start")
        self.about_button = Button(about_button_x, button_y, about_button_image, "about")

    def draw(self):
        # Draw the background image
        self.screen.blit(self.background_image, (0, 0))

        # Draw the buttons
        self.screen.blit(self.start_button.image, self.start_button.rect)
        self.screen.blit(self.about_button.image, self.about_button.rect)
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.rect.collidepoint(event.pos):
                    return "start_game"
                elif self.about_button.rect.collidepoint(event.pos):
                    return "about_screen"
        return "home_screen"
