import pygame

import colors

DEFAULT_FONT = 'freesansbold.ttf'

INF = 2 ** 16

# Super class of Info Tab
class InfoTab:
    def __init__(self, lock : bool, lifetime : float, text_pos : tuple[int, int]):
        self.lock_screen = lock
        self.text_pos = text_pos
        self.lifetime = lifetime

        # Ensure font is initialized
        if not pygame.font.get_init():
            pygame.font.init()

        # TODO: Allow for custom fonts?
        # Load the font
        self.font = pygame.font.Font(DEFAULT_FONT, 32)

    def render_text(self, msg : str, screen):
        text = self.font.render(msg, True, colors.white)
        text_rect = text.get_rect()

        text_rect.bottomleft = self.text_pos

        screen.blit(text, text_rect)

# Displays the list of commands
class InfoHelp(InfoTab):
    def __init__(self, text_pos : tuple[int, int]):
        super().__init__(False, 4.0, text_pos)

# Prompts the name of the save file (ESC to quit)
class InfoSave(InfoTab):
    def __init__(self, text_pos : tuple[int, int]):
        super().__init__(True, INF, text_pos)

# Prompts the name of the load file (ESC to quit)
class InfoLoad(InfoTab):
    def __init__(self, text_pos : tuple[int, int]):
        super().__init__(True, INF, text_pos)
