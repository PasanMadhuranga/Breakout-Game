import pygame
from pygame.sprite import Sprite


class Brick(Sprite):
    """A class to represent a single alien in the fleet"""

    def __init__(self, ai_game, color, brick_width):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = color

        # Create brick rect.
        self.brick_width = brick_width
        self.rect = pygame.Rect(0, 0, self.brick_width, self.settings.brick_height)

        # Start each new brick near the top left of the screen.
        self.rect.x = 0
        self.rect.y = 30

    def draw_brick(self):
        """Draw the brick to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)