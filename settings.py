class Settings:
    """A Class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        # Paddle settings
        self.paddle_width = 250
        self.paddle_height = 25
        self.paddle_color = (46, 134, 222)

        # Brick settings
        self.brick_color = (254, 202, 87)
        self.brick_height = 50

        # How quickly the game speeds up
        self.speedup_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.paddle_speed = 2.0
        self.ball_speed = [1, -1]


    def increase_speed(self):
        """Increase paddle speed"""
        self.paddle_speed *= self.speedup_scale