import pygame
from Data.data_handler import get_config
from Code.Scenes.scene import Intro, GameWorld
from Code.config import Config
import os
from debug import debug
from Code.support import timer

import time


class Game:
    def __init__(self):
        pygame.init()
        self.config = Config()
        self.config.load_config()
        self.display = pygame.display.set_mode((self.config.screen_width, self.config.screen_height))
        self.clock = pygame.time.Clock()
        self.game_stack = []
        self.actions = {"left": False, "right": False, "up": False, "down": False, "action1": False, "pause": False,
                        "menu": False}
        self.game_canvas = pygame.Surface((self.config.screen_width, self.config.screen_height))
        self.delta_time = 0
        self.prev_time = 0
        self.running = True

        self.timer = 0
        self.prev_time = 0
        self.dt = 0

        self.load_scene()
        self.load_assets()

    def set_screen(self):
        self.display = pygame.display.set_mode(
            (int(get_config("Display", "width")), int(get_config("Display", "height"))))

    def exit_game(self):
        self.running = False
        pygame.quit()
        exit()

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_game()
            if event.type == pygame.KEYDOWN:
                # if event.key == pygame.K_ESCAPE:
                #     self.running = False
                if event.key == pygame.K_a:
                    self.actions['left'] = True
                if event.key == pygame.K_d:
                    self.actions['right'] = True
                if event.key == pygame.K_w:
                    self.actions['up'] = True
                if event.key == pygame.K_s:
                    self.actions['down'] = True
                if event.key == pygame.K_SPACE:
                    self.actions['action1'] = True
                if event.key == pygame.K_ESCAPE:
                    self.actions['pause'] = True
                if event.key == pygame.K_TAB:
                    self.actions['menu'] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.actions['left'] = False
                if event.key == pygame.K_d:
                    self.actions['right'] = False
                if event.key == pygame.K_w:
                    self.actions['up'] = False
                if event.key == pygame.K_s:
                    self.actions['down'] = False
                if event.key == pygame.K_SPACE:
                    self.actions['action1'] = False
                    self.timer = pygame.time.get_ticks()
                if event.key == pygame.K_LSHIFT:
                    self.actions['pause'] = False
                if event.key == pygame.K_TAB:
                    self.actions['menu'] = False

    def reset_keys(self):
        for action in self.actions:
            self.actions[action] = False

    def update(self):
        self.game_stack[-1].update(self.delta_time, self.actions)

    def render(self):
        self.game_stack[-1].render(self.game_canvas)
        # Render current state to the screen
        self.display.blit(self.game_canvas, (0, 0))
        pygame.display.update()

    def main_loop(self):
        while self.running:
            self.get_dt()
            self.event_loop()
            self.update()
            self.render()
            self.clock.tick(60)

    def load_scene(self):
        self.game_stack.append(GameWorld(self))

    def get_dt(self):
        now = time.time()
        self.dt = now - self.prev_time
        self.prev_time = now

    def load_assets(self):
        # Create pointers to directories
        self.resources_dir = os.path.join("../Resources")



if __name__ == '__main__':
    Game().main_loop()
