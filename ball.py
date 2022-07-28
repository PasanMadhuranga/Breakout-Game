import pygame
from pygame.sprite import Sprite


class Ball(Sprite):

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.speed = ai_game.settings.ball_speed

        # Hit with something flags.
        self.hit_with_paddle_top = False
        self.hit_with_paddle_right = False
        self.hit_with_paddle_left = False

        # get the ball image, change its size and place it at the midbottom of the screen.
        self.ball_img = pygame.image.load("circle.png").convert()
        self.size = self.ball_img.get_size()
        self.size = (self.size[0] * 1 / 90, self.size[1] * 1 / 90)
        self.ball_img = pygame.transform.scale(self.ball_img, self.size)
        self.ball_rect = self.ball_img.get_rect()
        self.ball_rect.midbottom = self.screen_rect.midbottom


    def update_ball(self):
        """Draw the ball at the new location"""
        self.ball_rect.x += self.speed[0]
        self.ball_rect.y += self.speed[1]

        # bounce the ball when it hits left, right or top of the screen.
        if self.ball_rect.left <= 0 or self.ball_rect.right >= self.settings.screen_width:
            self.speed[0] *= -1
        elif abs(self.ball_rect.top) <= 0:  # or self.ball_rect.bottom > self.settings.screen_height
            self.speed[1] *= -1
        # Bounce the ball when it hits the paddle.
        else:
            if self.hit_with_paddle_top and self.speed[1] > 0:
                self.speed[1] *= -1
                self.hit_with_paddle_top = False

            if self.hit_with_paddle_right and self.speed[0] < 0:
                self.speed[0] *= -1
                self.hit_with_paddle_right = False

            if self.hit_with_paddle_left and self.speed[0] > 0:
                self.speed[0] *= -1
                self.hit_with_paddle_left = False

        # draw the ball at its new location.
        self.screen.blit(self.ball_img, self.ball_rect)


