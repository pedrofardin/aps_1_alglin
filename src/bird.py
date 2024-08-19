import pygame
import pymunk

class Bird(pygame.sprite.Sprite):
    def __init__(self, space):
        super().__init__()
        self.body = pymunk.Body(1, 100)
        self.shape = pymunk.Circle(self.body, 20)
        self.shape.elasticity = 0.95
        self.shape.friction = 1.0
        space.add(self.body, self.shape)
        
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.launched = False

    def launch(self, x_vel, y_vel):
        self.body.velocity = (x_vel, y_vel)
        self.launched = True

    def update(self):
        self.rect.center = self.body.position

class RedBird(Bird):
    def __init__(self, space):
        super().__init__(space)
        self.image = pygame.image.load("red_bird.png")
        self.image = pygame.transform.scale(self.image, (40, 40))

class BlueBird(Bird):
    def __init__(self, space):
        super().__init__(space)
        self.image = pygame.image.load("blue_bird.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))

    def special_ability(self):
        new_birds = [BlueBird(self.body._space) for _ in range(2)]
        for new_bird in new_birds:
            new_bird.body.position = self.body.position
            new_bird.body.velocity = (self.body.velocity.x * 0.8, self.body.velocity.y * 1.2)
            new_bird.launched = True
        return new_birds