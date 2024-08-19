import pygame

class Game:
    def __init__(self):
        self.score = 0
        self.level = 1
        self.birds_left = 3

    def add_score(self, points):
        self.score += points

    def next_level(self):
        self.level += 1
        self.birds_left = 3

    def draw_ui(self, screen):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (0, 0, 0))
        level_text = font.render(f"Level: {self.level}", True, (0, 0, 0))
        birds_text = font.render(f"Birds left: {self.birds_left}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 50))
        screen.blit(birds_text, (10, 90))