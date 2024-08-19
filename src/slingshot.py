import pygame
import math
from constants import HEIGHT

class Slingshot:
    def __init__(self):
        self.position = (100, HEIGHT - 100)
        self.pulled = False
        self.pull_position = None

    def draw(self, screen):
        pygame.draw.line(screen, (139, 69, 19), self.position, (self.position[0] - 20, self.position[1] + 50), 10)
        pygame.draw.line(screen, (139, 69, 19), self.position, (self.position[0] + 20, self.position[1] + 50), 10)
        if self.pulled:
            pygame.draw.line(screen, (189, 189, 189), self.position, self.pull_position, 5)

    def pull(self, position):
        self.pulled = True
        self.pull_position = position

    def release(self):
        self.pulled = False
        return self.calculate_launch_vector()

    def calculate_launch_vector(self):
        if not self.pull_position:
            return (0, 0)
        dx = self.position[0] - self.pull_position[0]
        dy = self.position[1] - self.pull_position[1]
        distance = math.sqrt(dx**2 + dy**2)
        power = min(distance / 10, 20)  # Limite máximo de potência
        angle = math.atan2(dy, dx)
        return (power * math.cos(angle), power * math.sin(angle))