import pygame
from Code.support import timer


class Transition:
    def __init__(self, display_surface: pygame.Surface, duration):
        self.display_surface = display_surface
        self.surface = pygame.Surface(display_surface.get_size(), flags=pygame.SRCALPHA)
        self.bg_color = "#262626"
        self.duration = duration
        self.speed = None
        self.start_time = None
        self.type = None

    def update(self): ...

    def play(self, dt) -> bool:
        """
        Play the transition based in the type
        :param dt: delta time from game loop
        :return: True if the transition ends, False if not
        """
        # Check if the transition start time is already set
        if not self.start_time:
            self.start_time = pygame.time.get_ticks()
        if self.type == "Fade":
            # Calculate the speed based in the duration
            self.speed = 240 / (self.duration / dt)
            self.update()
            self.display_surface.blit(self.surface, (0, 0))
            if timer(self.start_time, self.duration):
                return True
            return False


class FadeIn(Transition):
    def __init__(self, surface, duration):
        super().__init__(surface, duration)
        # Set the type and the alpha
        self.type = "Fade"
        self.alpha = 240

    def update(self):
        # Fill the surface with a bg color
        self.surface.fill(self.bg_color)
        # Set the alpha to make it transparent
        self.surface.set_alpha(self.alpha)
        # While the alpha is grater than 0, decrease it based in the speed
        if self.alpha > 0:
            self.alpha -= self.speed


class FadeOut(Transition):
    def __init__(self, surface, duration):
        super().__init__(surface, duration)
        # Set the type and the alpha
        self.type = "Fade"
        self.alpha = 0

    def update(self):
        # Fill the surface with a bg color
        self.surface.fill(self.bg_color)
        # Set the alpha to make it transparent
        self.surface.set_alpha(self.alpha)
        # While the alpha is less than 240, increase it based in the speed
        if self.alpha <= 240:
            self.alpha += self.speed
