import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

class ForceVisualizer:
    def __init__(self, screen, bird):
        self.screen = screen
        self.bird = bird

    def draw_vector(self, start_pos, vector, color, label):
        end_pos = (start_pos[0] + vector[0], start_pos[1] + vector[1])

        # desenha modulo e direção da força
        pygame.draw.line(self.screen, color, start_pos, end_pos, 5)
        pygame.draw.circle(self.screen, color, end_pos, 7)

        # escreve o tipo de força
        font = pygame.font.Font(None, 24)
        label_surface = font.render(label, True, color)
        label_rect = label_surface.get_rect(center=(end_pos[0] + 20, end_pos[1] + 10))
        self.screen.blit(label_surface, label_rect)

    def visualize_forces(self):
        vx = self.bird.velocity[0]
        vy = self.bird.velocity[1]

        # escala ajusatada dos vetores para visualização
        scale_velocity = 5
        scale_gravity = 5
        scale_elastic = 0.7

        # vetor da gravidade
        gravity_vector = [0, self.bird.gravity * scale_gravity]
        self.draw_vector(self.bird.rect.center, gravity_vector, (255, 0, 0), "Gravidade")

        # vetores da velocidade
        velocity_vector = [vx * scale_velocity, vy * scale_velocity]
        velocity_vector_x = [vx * scale_velocity, 0]
        velocity_vector_y = [0, vy * scale_velocity]
        if not self.bird.not_released:
            self.draw_vector(self.bird.rect.center, velocity_vector, (0, 255, 0), "Velocidade")
            self.draw_vector(self.bird.rect.center, velocity_vector_x, (0, 255, 0), "Vx")
            self.draw_vector(self.bird.rect.center, velocity_vector_y, (0, 255, 0), "Vy")

        # desenha a forca elastica
        if self.bird.dragging:
            drag_start = self.bird.drag_start_pos
            current_pos = self.bird.rect.center
            elastic_vector = [(drag_start[0] - current_pos[0]) * scale_elastic, 
                              (drag_start[1] - current_pos[1]) * scale_elastic]
            self.draw_vector(self.bird.rect.center, elastic_vector, (0, 0, 255), "Elasticity")
