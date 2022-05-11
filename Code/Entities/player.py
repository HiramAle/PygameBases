import pygame
from Code.support import import_cut_graphics
from Code.Entities.entity import Entity


class Player(Entity):
    def __init__(
            self,
            position: tuple,
            facing: str,
            groups: pygame.sprite.Group,
            obstacle_sprites: pygame.sprite.Group):
        super().__init__(
            groups,
            import_cut_graphics("Sprites/Player/player_down_idle.png", 64, 64 * 2)[0],
            obstacle_sprites
        )
        self.sprite_type = "player"
        # graphics
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = pygame.Rect(self.rect.x, self.rect.y, 64, 64)
        # status
        self.facing = facing
        self.status = self.facing + "_idle"
        # assets
        self.import_assets()
        self.animation_speed = 0.08

    def import_assets(self):
        self.animations = {"down": import_cut_graphics("Sprites/Player/player_down_run.png", 64, 64 * 2),
                           "up": import_cut_graphics("Sprites/Player/player_up_run.png", 64, 64 * 2),
                           "left": import_cut_graphics("Sprites/Player/player_left_run.png", 64, 64 * 2),
                           "right": import_cut_graphics("Sprites/Player/player_right_run.png", 64, 64 * 2),
                           "down_idle": import_cut_graphics("Sprites/Player/player_down_idle.png", 64, 64 * 2),
                           "up_idle": import_cut_graphics("Sprites/Player/player_up_idle.png", 64, 64 * 2),
                           "left_idle": import_cut_graphics("Sprites/Player/player_left_idle.png", 64, 64 * 2),
                           "right_idle": import_cut_graphics("Sprites/Player/player_right_idle.png", 64, 64 * 2)}

    def set_status(self):
        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if "idle" not in self.status:
                self.status += "_idle"
        # set facing direction
        if "right" in self.status:
            self.facing = "right"
        elif "left" in self.status:
            self.facing = "left"
        elif "down" in self.status:
            self.facing = "down"
        elif "up" in self.status:
            self.facing = "up"

    def animate_sprite(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def input(self, actions):
        # keys = pygame.key.get_pressed()

        if actions["up"] and not actions["down"]:
            self.direction.y = -1
            self.status = "up"
        elif actions["down"] and not actions["up"]:
            self.direction.y = 1
            self.status = "down"
        else:
            self.direction.y = 0

        if actions["left"] and not actions["right"]:
            self.direction.x = -1
            self.status = "left"
        elif actions["right"] and not actions["left"]:
            self.direction.x = 1
            self.status = "right"
        else:
            self.direction.x = 0

    def update(self):
        # self.input()
        self.set_status()
        self.animate_sprite()
        self.move()
