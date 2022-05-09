import pygame


class Menu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.get_surface()
        self.running = True
        self.clock = pygame.time.Clock()


# class MainMenu(Menu):
#     def __init__(self):
#         super().__init__()
#         self.btn_play = TextButton(100, 100, "Play")
#         self.fadein = FadeIn()
#         self.fadeout = FadeOut()
#         self.exit = False
#
#     def run(self):
#         while self.running:
#             for event in pygame.event.get():
#                 # exit check
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                     exit()
#
#             self.screen.fill("#262626")
#             self.btn_play.draw()
#
#             if self.btn_play.check_click():
#                 self.exit = True
#
#             if self.exit:
#                 self.fadeout.start()
#                 if self.fadeout.end:
#                     self.running = False
#
#             if not self.fadein.end:
#                 self.fadein.start()
#
#             pygame.display.update()
#             self.clock.tick(60)
