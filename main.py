import random
import sys
import time
import pygame
from settings import Settings
from paddle import Paddle
from ball import Ball
from bricks import Brick
from scoreboard import Scoreboard
from button import Button

BRICK_COLORS = ['#c0392b', '#e74c3c', '#f39c12', '#f1c40f', '#6ab04c', '#badc58']


class BreakoutGame:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """initialize the game, and create game resources"""
        pygame.init()

        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Breakout Game")

        self.paddle = Paddle(self)
        self.sb = Scoreboard(self)
        self.bricks = pygame.sprite.Group()

        # Create six sets of bricks.
        self._create_bricks_set()

        # Make the play button.
        self.play_button = Button(self, "Play")

        self.game_active = False


    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            if self.game_active:
                self.paddle.update()
            self._update_screen()
            # sleep time. this decreases with player's level.
            time.sleep(0.002 / self.sb.level)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # Reset the game settings
            self.settings.initialize_dynamic_settings()

            self.game_active = True
            # reset level, score and high score.
            self.sb.reset_all()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_high_score()

            # create the ball.
            self.ball = Ball(self)

            # empty the bricks set and create a new set.
            self.bricks.empty()
            self._create_bricks_set()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.paddle.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.paddle.moving_left = True
        elif event.key == pygame.K_ESCAPE:
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to keyreleases."""
        if event.key == pygame.K_RIGHT:
            self.paddle.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.paddle.moving_left = False

    def _check_paddle_ball_collisions(self):
        """Bounce the ball, when it hits a paddle."""
        if self.ball.ball_rect.colliderect(self.paddle.rect):
            self.ball.hit_with_paddle_top = abs(self.ball.ball_rect.bottom - self.paddle.rect.top) < 10
            self.ball.hit_with_paddle_left = abs(self.ball.ball_rect.right - self.paddle.rect.left) < 10
            self.ball.hit_with_paddle_right = abs(self.ball.ball_rect.left - self.paddle.rect.right) < 10

    def _check_ball_brick_collisions(self):
        for brick in self.bricks.sprites():
            if self.ball.ball_rect.colliderect(brick.rect):
                # Bounce the ball relevant to the collision side with a brick.
                if abs(self.ball.ball_rect.top - brick.rect.bottom) < 10 and self.ball.speed[1] < 0:
                    self.ball.speed[1] *= -1
                elif abs(self.ball.ball_rect.bottom - brick.rect.top) < 10 and self.ball.speed[1] > 0:
                    self.ball.speed[1] *= -1
                elif abs(self.ball.ball_rect.left - brick.rect.right) < 10 and self.ball.speed[0] < 0:
                    self.ball.speed[0] *= -1
                elif abs(self.ball.ball_rect.right - brick.rect.left) < 10 and self.ball.speed[0] > 0:
                    self.ball.speed[0] *= -1
                # remove the collided brick.
                brick.kill()
                # increase the score (according to the player's level)
                self.sb.score += 5 * self.sb.level
                self.sb.prep_score()
                # check whether current score is greater than high score.
                self.sb.check_high_score()

        if not self.bricks:
            # if all the bricks are over, increase the level and create a new sets of bricks and kill the old ball
            # and create a new ball at the midbottom of the increase.
            self.sb.level += 1
            self.sb.prep_level()
            self.ball.kill()
            self.ball = Ball(self)
            self._create_bricks_set()
            self.settings.increase_speed()

    def _check_miss_the_ball(self):
        """Check if the paddle misses the ball at the bottom."""
        if self.ball.ball_rect.bottom > self.settings.screen_height + 20:
            # update the new high score to the txt while.
            self.sb.update_high_score()
            self.game_active = False
            pygame.mouse.set_visible(True)
            self.ball.kill()

    def _create_bricks_set(self):
        """Create 6 rows of bricks."""
        for row_number in range(len(BRICK_COLORS), 0, -1):
            total_brick_length = 0
            while total_brick_length < self.settings.screen_width - 250:
                brick_width = self._create_brick(total_brick_length, row_number)
                total_brick_length += brick_width + 7
            # create last brick of the row.
            last_brick_width = self.settings.screen_width - total_brick_length
            self._create_brick(total_brick_length, row_number, last_brick_width)

    def _create_brick(self, total_brick_length, row_number, width=None):
        """Create a brick and place it in the row next to the last brick"""
        if not width:
            brick = Brick(self, BRICK_COLORS[row_number - 1], brick_width=random.randint(80, 220))
        else:
            brick = Brick(self, BRICK_COLORS[row_number - 1], width)

        brick_width, brick_height = brick.rect.size
        brick.rect.x = total_brick_length
        brick.rect.y = 3 + (brick_height + 7) * row_number
        self.bricks.add(brick)
        return brick_width

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.paddle.draw_paddle()
        self.sb.show_score()

        if self.game_active:
            self._check_paddle_ball_collisions()
            self._check_ball_brick_collisions()
            self._check_miss_the_ball()
            self.ball.update_ball()

        for brick in self.bricks.sprites():
            brick.draw_brick()

        # Draw the play button if the game is inactive.
        if not self.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = BreakoutGame()
    ai.run_game()