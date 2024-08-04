from typing import Literal, TypeVar, Any
from enum import Enum

import pygame as pg

version = '1.0.1'
ver = version

_KT = TypeVar('_KT')
_VT = TypeVar('_VT')

def reverse_dict(dictionary: dict[_KT, _VT]) -> dict[_VT, _KT]:
    '''
    Reverses a dictionary.

    dictionary: The dictionary to reverse.

    ---

    Example:
      >>> reverse_dict({'a': 'b', 'c': 'd'})
      {'b': 'a', 'd': 'c'}
    '''

    return {v: k for k, v in dictionary.items()}

keytopgkey = {
    'a': pg.K_a,
    'b': pg.K_b,
    'c': pg.K_c,
    'd': pg.K_d,
    'e': pg.K_e,
    'f': pg.K_f,
    'g': pg.K_g,
    'h': pg.K_h,
    'i': pg.K_i,
    'j': pg.K_j,
    'k': pg.K_k,
    'l': pg.K_l,
    'm': pg.K_m,
    'n': pg.K_n,
    'o': pg.K_o,
    'p': pg.K_p,
    'q': pg.K_q,
    'r': pg.K_r,
    's': pg.K_s,
    't': pg.K_t,
    'u': pg.K_u,
    'v': pg.K_v,
    'w': pg.K_w,
    'x': pg.K_x,
    'y': pg.K_y,
    'z': pg.K_z,
    '0': pg.K_0,
    '1': pg.K_1,
    '2': pg.K_2,
    '3': pg.K_3,
    '4': pg.K_4,
    '5': pg.K_5,
    '6': pg.K_6,
    '7': pg.K_7,
    '8': pg.K_8,
    '9': pg.K_9,
    ' ': pg.K_SPACE,
    '-': pg.K_MINUS,
    '=': pg.K_EQUALS,
    ';': pg.K_SEMICOLON,
    "'": pg.K_QUOTE,
    '[': pg.K_LEFTBRACKET,
    ']': pg.K_RIGHTBRACKET,
    '\\': pg.K_BACKSLASH,
    ',': pg.K_COMMA,
    '.': pg.K_PERIOD,
    '/': pg.K_SLASH,
    '`': pg.K_BACKQUOTE,
    '!': pg.K_EXCLAIM,
    '@': pg.K_AT,
    '#': pg.K_HASH,
    '$': pg.K_DOLLAR,
    '%': pg.K_PERCENT,
    '^': pg.K_CARET,
    '&': pg.K_AMPERSAND,
    '*': pg.K_ASTERISK,
    '(': pg.K_LEFTPAREN,
    ')': pg.K_RIGHTPAREN,
    '_': pg.K_UNDERSCORE,
    '+': pg.K_PLUS,
    'f1': pg.K_F1,
    'f2': pg.K_F2,
    'f3': pg.K_F3,
    'f4': pg.K_F4,
    'f5': pg.K_F5,
    'f6': pg.K_F6,
    'f7': pg.K_F7,
    'f8': pg.K_F8,
    'f9': pg.K_F9,
    'f10': pg.K_F10,
    'f11': pg.K_F11,
    'f12': pg.K_F12,
    'f13': pg.K_F13,
    'f14': pg.K_F14,
    'f15': pg.K_F15,
    'down': pg.K_DOWN,
    'up': pg.K_UP,
    'left': pg.K_LEFT,
    'right': pg.K_RIGHT,
    'esc': pg.K_ESCAPE,
    'enter': pg.K_RETURN,
    'tab': pg.K_TAB,
    'backspace': pg.K_BACKSPACE,
    'delete': pg.K_DELETE,
    'capslock': pg.K_CAPSLOCK,
    'lshift': pg.K_LSHIFT,
    'rshift': pg.K_RSHIFT,
    'lctrl': pg.K_LCTRL,
    'rctrl': pg.K_RCTRL,
    'lalt': pg.K_LALT,
    'ralt': pg.K_RALT,
    'space': pg.K_SPACE,
    'return': pg.K_RETURN
}

pgkeytokey = reverse_dict(keytopgkey)

mbtopgmb = {
    'lmb': 1,
    'rmb': 3,
    'mmb': 2,
    'scrollup': 4,
    'scrolldown': 5
}

pgmbtomb = reverse_dict(mbtopgmb)

key = Literal[
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
    'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
    'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3',
    '4', '5', '6', '7', '8', '9', ' ', '-', '=', ';',
    "'", '[', ']', '\\', ',', '.', '/', '`', '!', '@',
    '#', '$', '%', '^', '&', '*', '(', ')', '_', '+',
    'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
    'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'down', 'up',
    'left', 'right', 'esc', 'enter', 'tab', 'backspace',
    'delete', 'capslock', 'lshift', 'rshift', 'lctrl',
    'rctrl', 'lalt', 'ralt', 'space', 'return'
]

mb = Literal[
    'lmb', 'rmb', 'mmb', 'scrollup', 'scrolldown'
]

class colors:
    '''
    A class for storing color codes.
    '''

    BLACK = '\u001b[30m'
    RED = '\u001b[31m'
    GREEN = '\u001b[32m'
    YELLOW = '\u001b[33m'
    BLUE = '\u001b[34m'
    MAGENTA = '\u001b[35m'
    CYAN = '\u001b[36m'
    WHITE = '\u001b[37m'
    RESET = '\u001b[0m'
    LIGHT_BLACK = '\u001b[90m'
    LIGHT_RED = '\u001b[91m'
    LIGHT_GREEN = '\u001b[92m'
    LIGHT_YELLOW = '\u001b[93m'
    LIGHT_BLUE = '\u001b[94m'
    LIGHT_MAGENTA = '\u001b[95m'
    LIGHT_CYAN = '\u001b[96m'
    LIGHT_WHITE = '\u001b[97m'

    def __setattr__(self, name: str, value: Any, /) -> None:
        try:
            getattr(self, name)
            raise AttributeError(f'Cannot set attribute {name} to value {value} as it is constant')
        except AttributeError:
            raise

class attrs:
    '''
    A class for storing text attributes.
    '''
    
    BOLD = '\u001b[1m'
    UNDERLINE = '\u001b[4m'
    REVERSE = '\u001b[7m'
    CONCEALED = '\u001b[8m'
    STRIKETHROUGH = '\u001b[9m'
    RESET = '\u001b[0m'

    def __setattr__(self, name: str, value: Any, /) -> None:
        try:
            getattr(self, name)
            raise AttributeError(f'Cannot set attribute {name} to value {value} as it is constant')
        except AttributeError:
            raise