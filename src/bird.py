import pygame
import math
import pygame
import math

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y, images, mass=1.0):
        super().__init__()
        self.images = images if isinstance(images, list) else [images]
        self.current_frame = 0
        self.image = self.images[self.current_frame]

        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity = [0, 0]
        self.dragging = False
        self.not_released = True
        
        self.gravity = 2
        self.mass = mass  # Default mass of the bird

        self.drag_start_pos = (0, 0)
        self.max_drag_distance = 150

    def update(self):
        if self.dragging:
            mouse_pos = pygame.mouse.get_pos()
            # calcula a distância entre a posição do mouse e a posição inicial do arrasto
            distance = ((mouse_pos[0] - self.drag_start_pos[0]) ** 2 + (mouse_pos[1] - self.drag_start_pos[1]) ** 2) ** 0.5
            if distance > self.max_drag_distance:
                # Limit the drag distance

                # funcao que calcula o angulo em radianos pela arcotangente de y e x
                angle = math.atan2(mouse_pos[1] - self.drag_start_pos[1], mouse_pos[0] - self.drag_start_pos[0]) 
                mouse_pos = (
                    self.drag_start_pos[0] + self.max_drag_distance * math.cos(angle),
                    self.drag_start_pos[1] + self.max_drag_distance * math.sin(angle)
                )

            self.rect.center = mouse_pos
        else:
            self.rect.x += self.velocity[0]
            self.rect.y += self.velocity[1]

        if len(self.images) > 1:
            self.image = self.images[self.current_frame]

    def start_drag(self):
        self.dragging = True
        self.drag_start_pos = self.rect.center

    def end_drag(self):
        self.dragging = False
        self.not_released = False
        mouse_pos = pygame.mouse.get_pos()

        # Calcula a direção e a velocidade do pássaro
        direction = math.atan2(self.drag_start_pos[1] - mouse_pos[1], self.drag_start_pos[0] - mouse_pos[0])
        speed = ((self.drag_start_pos[0] - mouse_pos[0]) ** 2 + (self.drag_start_pos[1] - mouse_pos[1]) ** 2) ** 0.5 / 10
        #divisão por 10 para ajustar a velocidade.

        self.velocity = [speed * math.cos(direction), speed * math.sin(direction)]

    def hit_enemy(self, score):
        return score + 100 