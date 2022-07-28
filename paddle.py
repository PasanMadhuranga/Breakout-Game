import pygame
from pygame.sprite import Sprite


class Paddle(Sprite):
    """A class to manage the paddle."""

    def __init__(self, ai_game):
        super().__init__()

        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.color = self.settings.paddle_color

        # Create the paddle at the middle bottom of the screen.
        self.rect = pygame.Rect(0, 0,
                                self.settings.paddle_width, self.settings.paddle_height)
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.x += 300

        # Store a decimal value for the paddle's horizontal position
        self.x = float(self.rect.x)

        # Movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the paddle's position based on the movement flag."""
        # Update the paddle's x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.paddle_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.paddle_speed

        # Update the rect object from self.x.
        self.rect.x = self.x

    def draw_paddle(self):
        """Draw the paddle to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)