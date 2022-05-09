import pygame


class Button:
    def __init__(self, x, y, display):
        # Button position
        self.x = x
        self.y = y
        # Target display
        self.display = display
        # Button state
        self.pressed = False
        # Button rect
        self.rect = pygame.Rect(x, y, 50, 10)

    def hover(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            return True
        else:
            return False



class TextButton(Button):
    def __init__(self, x, y, display, text, colour="White", antialiasing=False, background=None,
                 font_path="../Resources/Fonts/pokemon_pixel_font.ttf", font_size=20, hover_colour="#D74B4B"):
        super().__init__(x, y, display)
        # font
        self.font = pygame.font.Font(font_path, font_size)
        self.font2 = pygame.font.Font(font_path, font_size+2)
        # text
        self.text = text
        self.text_surface = self.font.render(text, antialiasing, colour, background)
        self.rect = self.text_surface.get_rect(center=(x, y))

        self.text_aa = antialiasing
        self.text_colour = colour
        self.background = background
        self.before_hover_colour = self.text_colour
        self.hover_colour = hover_colour

    def check_click(self):
        if self.hover():
            self.text_colour = self.hover_colour
            action = False
            if self.hover():
                if pygame.mouse.get_pressed()[0] and not self.pressed:
                    self.pressed = True
                    action = True
                if not pygame.mouse.get_pressed()[0]:
                    self.pressed = False
            else:
                self.pressed = False

            return action
        else:
            self.text_colour = self.before_hover_colour

    def draw(self):
        self.text_surface = self.font.render(self.text, self.text_aa, self.text_colour, self.background)
        self.rect = self.text_surface.get_rect(center=(self.x, self.y))

        shadow_surface = self.font2.render(self.text, self.text_aa, "grey", self.background)
        shadow_rect = self.text_surface.get_rect(center=(self.x+4, self.y+2))
        self.display.blit(shadow_surface, shadow_rect)
        self.display.blit(self.text_surface, self.rect)


