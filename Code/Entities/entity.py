import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self,
                 groups: pygame.sprite.Group | list[pygame.sprite.Group],
                 image: pygame.surface.Surface,
                 obstacle_sprites: pygame.sprite.Group,
                 hit_box_w=64,
                 hit_box_h=64):
        super().__init__(groups)
        # graphics setup
        self.image = image
        self.rect = self.image.get_rect()
        self.hitbox = pygame.Rect(self.rect.x, self.rect.y, hit_box_w, hit_box_h)
        # movement
        self.direction = pygame.math.Vector2()
        self.speed = 5
        # collision sprites
        self.obstacle_sprites = obstacle_sprites
        # animation
        self.animations = {}
        self.frame_index = 0
        self.animation_speed = 0.6

    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * self.speed
        self.collision_x()
        self.hitbox.y += self.direction.y * self.speed
        self.collision_y()
        self.rect.bottom = self.hitbox.bottom

    def collision_x(self):
        if self.direction.x != 0:
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

    def collision_y(self):
        if self.direction.y != 0:
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
