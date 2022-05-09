import pygame
import copy
from Code.Entities.player import Player


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self, display, background):
        super().__init__()
        self.display_surface = display
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        self.floor_surf = background
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def y_draw(self, player: Player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.hitbox.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

        for sprite in player.obstacle_sprites:
            offset_pos = sprite.rect.topleft - self.offset
            hitbox = copy.copy(sprite.hitbox)
            hitbox.x = sprite.rect.x - offset_pos.x
            hitbox.y = sprite.rect.y - offset_pos.y
            pygame.draw.rect(pygame.display.get_surface(), "Red", hitbox, 2)
