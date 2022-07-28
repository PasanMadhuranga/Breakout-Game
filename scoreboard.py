import pygame.font


class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings

        # get the current highscore from the text file.
        with open("high_score.txt") as file:
            self.high_score = int(file.read().strip())

        self.score = 0
        self.level = 1

        # Font settings for scoring information.
        self.text_color = (236, 240, 241)
        self.font = pygame.font.SysFont(None, 30)

        # Prepare the initial score images.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()

    def prep_score(self):
        """Turn the score into a rendered image."""
        score_str = "Score: " + "{:,}".format(self.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score_str = "High Score: " + "{:,}".format(self.high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        # Center the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = "level: " + str(self.level)
        self.level_image = self.font.render(level_str, True,
                                            self.text_color, self.settings.bg_color)

        # Position the level on the left side of the screen.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.left = self.screen_rect.left + 20
        self.level_rect.top = self.score_rect.top

    def show_score(self):
        """Draw scores, high score and level to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.score > self.high_score:
            self.high_score = self.score
            self.prep_high_score()

    def update_high_score(self):
        """Write the new high score to the text file."""
        with open("high_score.txt", mode="w") as file:
            file.write(str(self.high_score))

    def reset_all(self):
        """Reset level and score."""
        self.score = 0
        self.level = 1
