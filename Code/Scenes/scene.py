import pygame
from Code.GUI.transitions import FadeIn, FadeOut
from Code.support import import_cut_graphics, get_center, timer
from Code.Entities.player import Player
from Code.Scenes.camera import YSortCameraGroup
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
        self.start_transition = FadeIn(game.game_canvas, 1)
        self.end_transitioning = False
        self.end_transition = FadeOut(game.game_canvas, 1)
        # Mouse cursor visibility
        pygame.mouse.set_visible(False)

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
        self.animations = import_cut_graphics("Sprites/intro.png", 96, 279)
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
        # Background
        self.background_image = pygame.image.load(
            os.path.join(self.game.resources_dir, "Images", "Start_menu_background.png"))
        # Box
        self.box = pygame.image.load(
            os.path.join(self.game.resources_dir, "Images", "Start_menu_box.png")).convert_alpha()
        self.box_rect = self.box.get_rect(topleft=(64, 394))
        # Texts
        x_text_offset = self.box_rect.x + 32 + (1120 / 3) / 2
        y_text_offset = self.box_rect.y + 32 + 90
        self.font = pygame.font.Font(os.path.join(self.game.resources_dir, "Fonts", "pokemon_pixel_font.ttf"), 100)
        self.text_play = self.font.render("Play", False, "#565656")
        self.text_play_rect = self.text_play.get_rect(center=(x_text_offset, y_text_offset))
        self.text_options = self.font.render("Options", False, "#565656")
        self.text_options_rect = self.text_play.get_rect(center=(x_text_offset + (1120 / 3), y_text_offset))
        self.text_exit = self.font.render("Exit", False, "#565656")
        self.text_exit_rect = self.text_play.get_rect(center=(x_text_offset + (1120 / 3) * 2, y_text_offset))
        # Cursor
        self.cursor_img = pygame.image.load(
            os.path.join(self.game.resources_dir, "Images", "cursor.png")).convert_alpha()
        self.cursor_rect = self.cursor_img.get_rect()
        self.cursor_y = self.box_rect.y + 100
        self.cursor_x = self.box_rect.x + 32 + 20
        self.cursor_rect.x, self.cursor_rect.y = self.cursor_x, self.cursor_y
        # Menu options
        self.menu_options = ["Play", "Options", "Exit"]
        self.index = 0

    def render_transition(self):
        # Check if the star transition is playing
        if self.start_transitioning:
            if self.start_transition.play(self.game.dt):
                self.start_transitioning = False
        elif self.end_transitioning:
            if self.end_transition.play(self.game.dt):
                GameWorld(self.game).enter_state()

    def update(self, delta_time, actions):

        if actions["space"]:
            if self.menu_options[self.index] == "Play":
                self.end_transitioning = True
            elif self.menu_options[self.index] == "Exit":
                self.game.exit_game()
        self.update_cursor(actions)

    def update_cursor(self, actions):
        if actions['right']:
            if self.index + 1 == len(self.menu_options):
                self.index = 0
            else:
                self.index += 1
        elif actions['left']:
            if not self.index:
                self.index = len(self.menu_options) - 1
            else:
                self.index -= 1
        self.game.reset_keys()

        self.cursor_rect.x = self.cursor_x + (self.index * (1120 / 3))

    def render(self, display: pygame.surface.Surface):
        display.blit(self.background_image, (0, 0))
        if not self.start_transitioning:
            display.blit(self.box, self.box_rect)
            display.blit(self.text_play, self.text_play_rect)
            display.blit(self.text_options, self.text_options_rect)
            display.blit(self.text_exit, self.text_exit_rect)
            display.blit(self.cursor_img, self.cursor_rect)

        self.render_transition()


class GameWorld(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.player_x, self.player_y = 100, 100
        self.bg_image = pygame.image.load(os.path.join(self.game.resources_dir, "Images","ground.png")).convert_alpha()
        self.visible_sprites = YSortCameraGroup(self.game.game_canvas, self.bg_image)
        self.obstacle_sprites = pygame.sprite.Group()
        self.player = Player(self.visible_sprites, (self.player_x, self.player_y), self.obstacle_sprites)

    def update(self, delta_time, actions):
        self.visible_sprites.update()
        self.player.update()

        if actions["pause"]:
            self.game.reset_keys()
            PauseMenu(self.game).enter_state()

    def render(self, display: pygame.surface.Surface):
        display.fill("#262626")
        self.visible_sprites.y_draw(self.player)
        # display.blit(self.player.image, (100, 100))
        # print(self.player.status)
        # print(self.player.animations[self.player.status])
        self.render_transition()

    def render_transition(self):
        # Check if the star transition is playing
        if self.start_transitioning:
            if self.start_transition.play(self.game.dt):
                self.start_transitioning = False


class Dialogue(Scene):
    def __init__(self, game):
        super().__init__(game)


class PauseMenu(Scene):
    def __init__(self, game):
        super().__init__(game)
        # Menu
        self.menu = pygame.image.load(os.path.join(self.game.resources_dir, "Images", "Pause_Menu.png")).convert_alpha()
        self.menu = pygame.transform.smoothscale(self.menu, (self.menu.get_size()[0], 500))
        self.menu_x = self.game.game_canvas.get_size()[0] - 20 - self.menu.get_size()[0]
        self.menu_y = self.game.game_canvas.get_size()[1] - (self.game.game_canvas.get_size()[1] / 2) - (
                self.menu.get_size()[1] / 2)
        self.menu_rect = self.menu.get_rect(topleft=(self.menu_x, self.menu_y))
        # Menu options
        self.menu_options = ["Option1", "Option2", "Option3", "Exit"]
        self.index = 0
        # Text
        x_text_offset = self.menu_rect.x + 50
        y_text_offset = self.menu_rect.y + 95
        self.font = pygame.font.Font(os.path.join(self.game.resources_dir, "Fonts", "pokemon_pixel_font.ttf"), 60)
        self.text_option = self.font.render("Option1", False, "#565656")
        self.text_option_rect = self.text_option.get_rect(midleft=(x_text_offset, y_text_offset))
        self.text_option2 = self.font.render("Option2", False, "#565656")
        self.text_option2_rect = self.text_option2.get_rect(midleft=(x_text_offset, y_text_offset + 100))
        self.text_option3 = self.font.render("Option3", False, "#565656")
        self.text_option3_rect = self.text_option3.get_rect(midleft=(x_text_offset, y_text_offset + (100 * 2)))
        self.text_exit = self.font.render("Exit", False, "#565656")
        self.text_exit_rect = self.text_exit.get_rect(midleft=(x_text_offset, y_text_offset + (100 * 3)))
        # Cursor
        self.cursor_img = pygame.image.load(
            os.path.join(self.game.resources_dir, "Images", "cursor.png")).convert_alpha()
        self.cursor_rect = self.cursor_img.get_rect()
        self.cursor_y = self.menu_rect.y + 80
        self.cursor_rect.x, self.cursor_rect.y = self.menu_rect.x + 20, self.cursor_y

    def update(self, delta_time, actions):
        self.update_cursor(actions)
        if actions["pause"]:
            self.exit_state()
            self.game.reset_keys()
        elif actions["space"]:
            if self.menu_options[self.index] == "Exit":
                self.game.game_stack = []
                Menu(self.game).enter_state()
        self.game.reset_keys()

    def update_cursor(self, actions):
        if actions['down']:
            if self.index + 1 == len(self.menu_options):
                self.index = 0
            else:
                self.index += 1

            self.game.reset_keys()
        elif actions['up']:
            if not self.index:
                self.index = len(self.menu_options) - 1
            else:
                self.index -= 1
            self.game.reset_keys()

        self.cursor_rect.y = self.cursor_y + (self.index * 100)

    def render(self, display: pygame.surface.Surface):
        self.prev_scene.render(display)
        display.blit(self.menu, self.menu_rect)
        display.blit(self.text_option, self.text_option_rect)
        display.blit(self.text_option2, self.text_option2_rect)
        display.blit(self.text_option3, self.text_option3_rect)
        display.blit(self.text_exit, self.text_exit_rect)
        display.blit(self.cursor_img, self.cursor_rect)
