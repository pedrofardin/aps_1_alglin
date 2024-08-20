import pygame
import sys
import random
import math
import numpy as np

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 700

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Angry Birds")

# Load bird images
player_bird_images = [pygame.transform.scale(pygame.image.load("player_bird.png"), (75, 75)),
                      pygame.transform.scale(pygame.image.load("red_bird.png"), (75, 75))]  # Replace path if needed
enemy_bird_image = pygame.transform.scale(pygame.image.load("enemy_bird.png"), (75, 75))    # Replace path if needed 

# Load background image
background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))


# Bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y, images):
        super().__init__()
        if isinstance(images, list):
            self.images = images
            self.current_frame = 1
            self.image = self.images[self.current_frame]
        else:
            self.images = [images]
            self.current_frame = 1
            self.image = images
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity = [0, 0]
        self.dragging = False
        self.drag_start_pos = (0, 0)
        self.gravity = 5
        self.not_released = True

    def update(self):
        if self.dragging:
            mouse_pos = pygame.mouse.get_pos()
            self.rect.centerx = mouse_pos[0]
            self.rect.centery = mouse_pos[1]
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
        direction = math.atan2(self.drag_start_pos[1] - mouse_pos[1], self.drag_start_pos[0] - mouse_pos[0])
        speed = math.hypot(self.drag_start_pos[1] - mouse_pos[1], self.drag_start_pos[0] - mouse_pos[0]) / 5
        self.velocity = [speed * math.cos(direction), speed * math.sin(direction)]

    def hit_enemy(self):
        global score
        score += 100  # Increase the score by 100 when an enemy is hit

# Button class
class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, image, action):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.action = action

# ForceVisualizer class
class ForceVisualizer:
    def __init__(self, screen, bird):
        self.screen = screen
        self.bird = bird

    def draw_vector(self, start_pos, vector, color, label):
        end_pos = (start_pos[0] + vector[0], start_pos[1] + vector[1])

        # Ensure the vector is within screen bounds
        end_pos = (max(0, min(end_pos[0], SCREEN_WIDTH)), 
                   max(0, min(end_pos[1], SCREEN_HEIGHT)))

        pygame.draw.line(self.screen, color, start_pos, end_pos, 5)
        pygame.draw.circle(self.screen, color, end_pos, 7)

        # Draw label text
        font = pygame.font.Font(None, 24)
        label_surface = font.render(label, True, color)
        label_rect = label_surface.get_rect(center=(end_pos[0] + 20, end_pos[1] + 10))
        self.screen.blit(label_surface, label_rect)

    def visualize_forces(self):
        vx = self.bird.velocity[0]
        vy = self.bird.velocity[1]

        # Adjusted scale factors for visibility
        scale_velocity = 5
        scale_gravity = 5
        scale_elastic = 0.5

        # Draw gravity vector
        gravity_vector = [0, self.bird.gravity * scale_gravity]
        self.draw_vector(self.bird.rect.center, gravity_vector, (255, 0, 0), "Gravity")

        # Draw velocity vector
        velocity_vector = [vx * scale_velocity, vy * scale_velocity]
        velocity_vector_x = [vx * scale_velocity, 0]
        velocity_vector_y = [0, vy * scale_velocity]
        if not self.bird.not_released:
            self.draw_vector(self.bird.rect.center, velocity_vector, (0, 255, 0), "Velocity")
            self.draw_vector(self.bird.rect.center, velocity_vector_x, (0, 255, 0), "Vx")
            self.draw_vector(self.bird.rect.center, velocity_vector_y, (0, 255, 0), "Vy")

        # Draw elastic force vector
        if self.bird.dragging:
            drag_start = self.bird.drag_start_pos
            current_pos = self.bird.rect.center
            elastic_vector = [(drag_start[0] - current_pos[0]) * scale_elastic, 
                              (drag_start[1] - current_pos[1]) * scale_elastic]
            self.draw_vector(self.bird.rect.center, elastic_vector, (0, 0, 255), "Elasticity")

# Create player bird
player_bird = Bird(SCREEN_WIDTH // 5, SCREEN_HEIGHT * 4 // 5, player_bird_images)

# Create enemy birds
enemy_birds = pygame.sprite.Group()
for _ in range(5):
    x = random.randint(SCREEN_WIDTH // 2, SCREEN_WIDTH - 50)
    y = random.randint(50, SCREEN_HEIGHT - 50)
    enemy_bird = Bird(x, y, enemy_bird_image)
    enemy_birds.add(enemy_bird)

# Initialize ForceVisualizer
# force_visualizer = ForceVisualizer(screen, player_bird)

# Game loop
clock = pygame.time.Clock()

# Initialize player's score
score = 0

# Calculating button positions 
button_margin = 10
button_top = button_margin
button_left = button_margin
button_spacing = 5

# Calculate 1 inch offset in pixels (assuming standard DPI of 96)
score_position = (1260, 80)

# Create buttons
quit_button_image = pygame.image.load("quit_button.png")        # Replace path if needed
refresh_button_image = pygame.image.load("refresh_button.png")  # Replace path if needed

quit_button = Button(button_left, button_top, quit_button_image, "quit")
refresh_button = Button(button_left + quit_button_image.get_width() + button_spacing, button_top, refresh_button_image, "refresh")
screen.blit(quit_button.image, quit_button.rect.topleft)
screen.blit(refresh_button.image, refresh_button.rect.topleft)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Event handling code for buttons and player bird dragging
        if event.type == pygame.MOUSEBUTTONDOWN:
            if quit_button.rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

            elif refresh_button.rect.collidepoint(event.pos):
                player_bird.rect.center = (100, SCREEN_HEIGHT // 2)
                player_bird.velocity = [0, 0]
                enemy_birds.empty()
                for _ in range(5):
                    x = random.randint(SCREEN_WIDTH // 2, SCREEN_WIDTH - 50)
                    y = random.randint(50, SCREEN_HEIGHT - 50)
                    enemy_bird = Bird(x, y, enemy_bird_image)
                    enemy_birds.add(enemy_bird)
                score = 0

            elif player_bird.rect.collidepoint(event.pos):
                player_bird.start_drag()

        elif event.type == pygame.MOUSEBUTTONUP:
            if player_bird.dragging:
                player_bird.end_drag()

    if not player_bird.not_released:
        player_bird.velocity[1] += player_bird.gravity / 10

    if player_bird.dragging or not player_bird.not_released:
        player_bird.current_frame = 0
    else:
        player_bird.current_frame = 1

    # Check for collisions
    hits = pygame.sprite.spritecollide(player_bird, enemy_birds, True)
    if hits:
        for hit_enemy in hits:
            hit_enemy.hit_enemy()

    # Reset player bird if it goes out of screen
    if player_bird.rect.left > SCREEN_WIDTH or player_bird.rect.right < 0 or \
            player_bird.rect.top > SCREEN_HEIGHT or player_bird.rect.bottom < 0:
        player_bird.rect.center = (SCREEN_WIDTH // 5, SCREEN_HEIGHT * 4 // 5)
        player_bird.velocity = [0, 0]
        player_bird.not_released = True

    # Clear the screen and draw background
    screen.blit(background_image, (0, 0))

    # Update and draw player bird
    player_bird.update()
    screen.blit(player_bird.image, player_bird.rect)

    # Update and draw enemy birds
    enemy_birds.update()
    enemy_birds.draw(screen)

    # Visualize forces acting on the player bird
    # force_visualizer.visualize_forces()

    # Display the score
    font = pygame.font.Font(None, 50)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, score_position)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

