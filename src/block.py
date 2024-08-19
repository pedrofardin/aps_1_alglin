import pygame
import pymunk

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, space):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((150, 75, 0))  # Cor de madeira
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        moment = pymunk.moment_for_box(1, (width, height))
        self.body = pymunk.Body(1, moment)
        self.body.position = x + width/2, y + height/2
        self.shape = pymunk.Poly.create_box(self.body, (width, height))
        self.shape.elasticity = 0.5
        self.shape.friction = 0.5
        space.add(self.body, self.shape)

    def update(self):
        self.rect.center = self.body.position

def create_structure(x, y, space):
    blocks = pygame.sprite.Group()
    # Base
    for i in range(5):
        block = Block(x + i*40, y, 40, 40, space)
        blocks.add(block)
    # Segundo andar
    for i in range(3):
        block = Block(x + 40 + i*40, y - 40, 40, 40, space)
        blocks.add(block)
    # Topo
    block = Block(x + 80, y - 80, 40, 40, space)
    blocks.add(block)
    return blocks

def create_floor(space, width, height):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (width // 2, height - 10)
    shape = pymunk.Segment(body, (-width // 2, 0), (width // 2, 0), 10)
    shape.elasticity = 0.5
    shape.friction = 1.0
    space.add(body, shape)
    
    # Criar um sprite para representar visualmente o chão
    floor_sprite = pygame.sprite.Sprite()
    floor_sprite.image = pygame.Surface((width, 20))
    floor_sprite.image.fill((100, 100, 100))  # Cor cinza
    floor_sprite.rect = floor_sprite.image.get_rect()
    floor_sprite.rect.midbottom = (width // 2, height)
    
    return floor_sprite

