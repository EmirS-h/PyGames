import pygame
from pygame.math import Vector2


class Input:
    """
    A static Input Manager.
    Call Input.update() at the start of every frame in your game loop.
    """

    _keys = []
    _keys_just_pressed = []
    _mouse_buttons = []
    _mouse_just_pressed = []
    _mouse_pos = (0, 0)

    @staticmethod
    def update() -> None:
        # Get current states
        Input._keys = pygame.key.get_pressed()
        Input._keys_just_pressed = pygame.key.get_just_pressed()

        Input._mouse_buttons = pygame.mouse.get_pressed()
        Input._mouse_just_pressed = pygame.mouse.get_just_pressed()
        Input._mouse_pos = pygame.mouse.get_pos()

    @staticmethod
    def get_key(key_code: int) -> bool:
        """Returns True while the user holds down the key."""
        if not Input._keys:
            return False
        return Input._keys[key_code]

    @staticmethod
    def get_key_down(key_code: int) -> bool:
        """Returns True during the frame the user starts pressing the key."""
        if not Input._keys_just_pressed:
            return False
        return Input._keys_just_pressed[key_code]

    @staticmethod
    def get_axis(negative_key: int, positive_key: int) -> int:
        """
        Returns -1, 0, or 1 based on keys pressed.
        Useful for movement (e.g., Left/Right).
        """
        return int(Input.get_key(positive_key)) - int(Input.get_key(negative_key))

    @staticmethod
    def get_mouse_button(button_index: int) -> bool:
        """0 = Left, 1 = Middle, 2 = Right"""
        if not Input._mouse_buttons:
            return False
        return Input._mouse_buttons[button_index]

    @staticmethod
    def get_mouse_button_down(button_index: int) -> bool:
        """Returns True if mouse button was just clicked."""
        if not Input._mouse_just_pressed:
            return False
        return Input._mouse_just_pressed[button_index]

    @staticmethod
    def get_mouse_pos() -> Vector2:
        return Vector2(Input._mouse_pos)
