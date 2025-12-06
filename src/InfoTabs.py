import pygame

import colors

DEFAULT_FONT = 'freesansbold.ttf'

INF = 2 ** 16

# Super class of Info Tab
class InfoTab:
    def __init__(self, text_pos : tuple[int, int]):
        self.text_pos = text_pos

        self.__to_render = False
        self.lock_keyboard = True

        # Ensure font is initialized
        if not pygame.font.get_init():
            pygame.font.init()

        # Load the font
        self.font = pygame.font.Font(DEFAULT_FONT, 20)

        self.background = None

    def load_background(self, screen):
        if self.background == None:
            self.background = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            self.background.fill(colors.dark)

    def set_to_render(self, to_render : bool):
        self.__to_render = to_render

    def toggle_render(self):
        self.__to_render = not self.__to_render

    def to_render(self):
        return self.__to_render

    def render_background(self, screen):
        if self.__to_render:
            self.load_background(screen)
            screen.blit(self.background, (0, 0))

    def render(self, screen):
        self.render_background(screen)

# Displays the list of commands
class InfoHelp(InfoTab):
    def __init__(self, text_pos : tuple[int, int]):
        super().__init__(text_pos)

        self.str_list : list[str] = ["Info about keybinds:",
                                "Ctrl + h -> opens/closes this screen",
                                "Ctrl + v -> shows/hides the editor GUI",
                                "Ctrl + z -> undo last action",
                                "Ctrl + y -> redo last action",
                                "Ctrl + s -> opens/closes save screen",
                                "Ctrl + Shift + s -> saves the map under the current name",
                                "Ctrl + l -> opens/closes load screen",
                                "Esc -> close any info screen"]

        self.text_surface = None

    def render_text(self, screen):
        if self.text_surface == None:
            self.text_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

            x = self.text_pos[0]
            y = self.text_pos[1]

            for line in self.str_list:
                text = self.font.render(line, True, colors.white)
                text_rect = text.get_rect()

                text_rect.x = x
                text_rect.y = y

                y += text_rect.height * 2

                self.text_surface.blit(text, text_rect)

    def render(self, screen):
        if self.to_render():
            super().render(screen)
            self.render_text(screen)
            screen.blit(self.text_surface, (0, 0))

# Prompts the name of the save file
class InfoSave(InfoTab):
    def __init__(self, text_pos : tuple[int, int]):
        super().__init__(text_pos)

        self.map_name = ""
        self.lock_keyboard = False

        self.str_list : list[str] = ["Save map",
                                     "Enter map name below:"]

        self.text_surface = None

    def render_text(self, screen, map_name):
        if self.text_surface != None:
            del self.text_surface

        self.text_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

        x = self.text_pos[0]
        y = self.text_pos[1]

        for line in self.str_list:
            text = self.font.render(line, True, colors.white)
            text_rect = text.get_rect()

            text_rect.x = x
            text_rect.y = y

            y += text_rect.height * 2

            self.text_surface.blit(text, text_rect)

        text = self.font.render(map_name, True, colors.white)
        text_rect = text.get_rect()

        text_rect.x = x
        text_rect.y = y

        self.text_surface.blit(text, text_rect)

    def render_with_name(self, screen, map_name):
        if self.to_render():
            super().render(screen)
            self.render_text(screen, map_name)
            screen.blit(self.text_surface, (0, 0))

    def add_key(self, unicode, key, map_name : str):
        if key != pygame.K_BACKSPACE:
            map_name += unicode
        else:
            map_name = map_name[:-1]

        return map_name

# Prompts the name of the load file
class InfoLoad(InfoTab):
    def __init__(self, text_pos : tuple[int, int]):
        super().__init__(text_pos)

        self.str_list : list[str] = ["Load map",
                                     "Enter map name below:"]

        self.lock_keyboard = False

        self.text_surface = None

    def render_text(self, screen, map_name):
        if self.text_surface != None:
            del self.text_surface

        self.text_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

        x = self.text_pos[0]
        y = self.text_pos[1]

        for line in self.str_list:
            text = self.font.render(line, True, colors.white)
            text_rect = text.get_rect()

            text_rect.x = x
            text_rect.y = y

            y += text_rect.height * 2

            self.text_surface.blit(text, text_rect)

        text = self.font.render(map_name, True, colors.white)
        text_rect = text.get_rect()

        text_rect.x = x
        text_rect.y = y

        self.text_surface.blit(text, text_rect)

    def render_with_name(self, screen, map_name):
        if self.to_render():
            super().render(screen)
            self.render_text(screen, map_name)
            screen.blit(self.text_surface, (0, 0))

    def add_key(self, unicode, key, map_name : str):
        if key != pygame.K_BACKSPACE:
            map_name += unicode
        else:
            map_name = map_name[:-1]

        return map_name

