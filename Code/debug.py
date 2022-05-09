import pygame


def debug(text, x=10, y=10):
    screen = pygame.display.get_surface()
    font = pygame.font.Font(None, 30)
    debug_surf = font.render(str(text), True, "White")
    debug_rect = debug_surf.get_rect(topleft=(x, y))
    pygame.draw.rect(screen, "Black", debug_rect)
    screen.blit(debug_surf, debug_rect)

