import pygame
from Code.GUI.transitions import FadeIn, FadeOut
from Code.GUI.buttons import TextButton
from Code.support import import_cut_graphics, get_center, timer
import os


class Scene:
    def __init__(self, game):
        # stack handler
        self.game = game
        self.prev_scene = None
        # graphic handler
        self.bg_color = "#262626"
        self.bg_image_path = ""
        # player properties
        self.player_x = 0
        self.player_y = 0
        self.player_direction = pygame.math.Vector2()
        # sprites
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        # transitions
        self.start_transitioning = True
        self.start_transition = FadeIn(game.game_canvas, 1.5)
        self.end_transitioning = False
        self.end_transition = FadeOut(game.game_canvas, 1.5)

    def update(self, delta_time, actions): ...

    def render(self, display: pygame.surface.Surface): ...

    def render_transition(self): ...

    def enter_state(self):
        if len(self.game.game_stack) > 1:
            self.prev_scene = self.game.game_stack[-1]
        self.game.game_stack.append(self)

    def exit_state(self):
        self.game.game_stack.pop()


class Intro(Scene):
    def __init__(self, game):
        super().__init__(game)
        # Animation variables
        self.animation_speed = 0.1
        self.animations = []
        self.frame_index = 0
        self.animations = import_cut_graphics("../Resources/Sprites/intro.png", 96, 279)
        # Animation image
        self.image = self.animations[self.frame_index]
        # Center of the display
        self.center = get_center(self.image)
        # Scene duration
        self.scene_duration = 2
        # Set the start time for the scene
        self.start_time = pygame.time.get_ticks()

    def render_transition(self):
        # If it's transitioning, render the transition
        if self.end_transitioning:
            if self.end_transition.play(self.game.dt):
                # Start the next state and pop up the intro from the stack
                self.exit_state()
                Menu(self.game).enter_state()

    def update(self, delta_time, actions):
        # Set the state to transitioning if the timer ends based in the scene duration
        if timer(self.start_time, self.scene_duration):
            if not self.end_transitioning:
                self.end_transitioning = True

    def render(self, display: pygame.surface.Surface):
        # Clear the screen
        display.fill(self.bg_color)
        # Increase the animation frame
        self.frame_index += self.animation_speed
        # Checks if the animation frame is the last one
        if self.frame_index >= len(self.animations):
            # Restart the animation
            self.frame_index = 0
        # Set and blit the image
        self.image = self.animations[int(self.frame_index)]
        display.blit(self.image, (self.center[0], self.center[1]))
        # Render the transition if necessary
        self.render_transition()


class Menu(Scene):
    def __init__(self, game):
        super().__init__(game)
        # Get the measurements of the screen to place the buttons
        center_x, center_y = get_center()
        y_segments = game.game_canvas.get_size()[1] / 4
        # Initialize the buttons
        self.start_button = TextButton(center_x, y_segments, game.game_canvas, "Start", "White", False, font_size=100)

        self.options_button = TextButton(center_x, y_segments * 2, game.game_canvas, "Options", "White", False,
                                         font_size=100)
        self.exit_button = TextButton(center_x, y_segments * 3, game.game_canvas, "Exit", "White", False, font_size=100)

    def render_transition(self):
        # Check if the star transition is playing
        if self.start_transitioning:
            if self.start_transition.play(self.game.dt):
                self.start_transitioning = False
        elif self.end_transitioning:
            if self.end_transition.play(self.game.dt):
                GameWorld(self.game).enter_state()

    def update(self, delta_time, actions):
        # Check if any button get pressed only if it's not transitioning
        if not self.start_transitioning and not self.end_transitioning:
            if self.start_button.check_click():
                self.end_transitioning = True
            elif self.options_button.check_click():
                print("Pressed")
            elif self.exit_button.check_click():
                self.game.exit_game()

    def render(self, display: pygame.surface.Surface):
        # Clear the screen
        display.fill("#262626")
        # Draw the buttons
        self.start_button.draw()

        self.options_button.draw()
        self.exit_button.draw()
        # Render the transition if its necessary
        self.render_transition()


class GameWorld(Scene):
    def __init__(self, game):
        super().__init__(game)

    def update(self, delta_time, actions):
        if actions["pause"]:
            self.game.reset_keys()
            PauseMenu(self.game).enter_state()

    def render(self, display: pygame.surface.Surface):
        display.fill("#262626")
        self.render_transition()

    def render_transition(self): ...
    # Check if the star transition is playing
    # if self.start_transitioning:
    #     if self.start_transition.play(self.game.dt):
    #         self.start_transitioning = False


class PauseMenu(Scene):
    def __init__(self, game):
        super().__init__(game)
        height = (70 * self.game.game_canvas.get_size()[1]) / 100
        self.menu = pygame.image.load("../Resources/Images/cuadrao.png").convert_alpha()
        self.menu = pygame.transform.smoothscale(self.menu, (self.menu.get_size()[0], height))
        self.menu_x = self.game.game_canvas.get_size()[0] - 4 - self.menu.get_size()[0]
        self.menu_y = self.game.game_canvas.get_size()[1] - (self.game.game_canvas.get_size()[1] / 2) - (
                    self.menu.get_size()[1] / 2)
        self.menu_rect = self.menu.get_rect(topleft=(self.menu_x, self.menu_y))

        # self.menu_options = {0: "Party", 1: "Items", 2: "Magic", 3: "Exit"}
        self.menu_options = ["Party", "Items", "Magic", "Exit"]
        self.index = 0

        self.cursor_img = pygame.image.load(os.path.join(self.game.resources_dir, "Images", "cursor.png"))
        self.cursor_rect = self.cursor_img.get_rect()
        self.cursor_y = self.menu_rect.y + 40
        self.cursor_rect.x, self.cursor_rect.y = self.menu_rect.x + 20, self.cursor_y
        print(self.menu.get_size()[1])

    def update(self, delta_time, actions):
        self.update_cursor(actions)
        if actions["pause"]:
            self.exit_state()
            self.game.reset_keys()

    def update_cursor(self, actions):
        if actions['down']:
            print(self.index % len(self.menu_options))
            self.index = (self.index + 1) % len(self.menu_options)

            self.game.reset_keys()
        elif actions['up']:
            self.index = (self.index - 1) % len(self.menu_options)
            self.game.reset_keys()
        self.cursor_rect.y = self.cursor_y + (self.index * 100)

    def render(self, display: pygame.surface.Surface):
        display.blit(self.menu, self.menu_rect)
        display.blit(self.cursor_img, self.cursor_rect)
