import pygame
import Events

# Singleton for storing the keyboard state of the user
class KeyboardState:
    __instance = None
    __initialized = False

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        if not KeyboardState.__initialized:
            self.is_ctrl_hold = False
            self.key_pressed = None
            self.key_is_down = False
            KeyboardState.__initialized = True

    def parse_key_input(self, key, is_down : bool):
        # Handle special keys
        if key == pygame.K_LCTRL:
            self.is_ctrl_hold = is_down
        else:
            # Store the key pressed
            self.key_pressed = key
            self.key_is_down = is_down

        pygame.event.post(pygame.event.Event(Events.KEYBOARD_CHANGED))

