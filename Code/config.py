import pygame
from Code.Data.data_handler import get_config


class Config:
    def __init__(self):
        self.screen_width = 720
        self.screen_height = 1280

    def load_config(self):
        self.screen_width = int(get_config("Display", "width"))
        self.screen_height = int(get_config("Display", "height"))
