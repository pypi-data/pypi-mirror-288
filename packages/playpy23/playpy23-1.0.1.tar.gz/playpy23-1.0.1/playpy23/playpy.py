import os
import sys
from typing import Literal, Union

import pygame as pg
import time

from . import plp_utils as plpu

time.sleep(.1)

# clear the screen
print("\033[2J\033[H", end="", flush=True)

python_version = sys.version_info
version_text = f'{python_version.major}.{python_version.minor}.{python_version.micro}'

print(
f'{plpu.attrs.BOLD}PlayPy23 {plpu.version} (Python {version_text}, Pygame {pg.ver}){plpu.attrs.RESET}\n{plpu.colors.LIGHT_YELLOW}{plpu.attrs.BOLD}Welcome to PlayPy23!{plpu.colors.RESET} If you would like to share your games and ideas, join our community on Discord!\n\n{plpu.colors.BLUE}{plpu.attrs.UNDERLINE}https://discord.gg/XnRKWwMKBk{plpu.colors.RESET}'
)

class InitError(Exception):
    pass

imagePath = 'assets/images'
soundPath = 'assets/sounds'
fontPath = 'assets/fonts'
audio_free = False
initialized = False

def init():
    global imagePath, soundPath, fontPath, audio_free, initialized
    if initialized:
        raise InitError('PlayPy23 has already been initialized')
    pg.init()
    if not audio_free:
        try:
            pg.mixer.init()
        except pg.error as e:
            raise InitError('Error while initializing audio', *e.args) from None
    initialized = True
    file_error_text = 'To use PlayPy23, you must add the following directories to your project:\n\n'
    file_not_found = False
    usable_functions = []
    if not os.path.exists(imagePath):
        file_error_text += f'- {imagePath}\n'
        usable_functions.append('set_image_path()')
        file_not_found = True
    if not os.path.exists(soundPath) and not audio_free:
        file_error_text += f'- {soundPath}\n'
        usable_functions.append('set_sound_path()')
        file_not_found = True
    if not os.path.exists(fontPath):
        file_error_text += f'- {fontPath}\n'
        usable_functions.append('set_font_path()')
        file_not_found = True
    if file_not_found:
        path_text = "\n        - ".join(usable_functions)
        file_error_text += f'\nTo be able to use PlayPy23, you can either:\n\n    - add the missing directories to your project\n    - use the following functions to set the required paths:\n\n        - {path_text}'
        print(file_error_text)
        exit(1)

def set_image_path(path: str):
    global imagePath, initialized
    if initialized:
        raise InitError('Cannot change image path after PlayPy23 has been initialized')
    imagePath = path

def set_sound_path(path: str):
    global soundPath, initialized
    if initialized:
        raise InitError('Cannot change sound path after PlayPy23 has been initialized')
    soundPath = path

def set_font_path(path: str):
    global fontPath, initialized
    if initialized:
        raise InitError('Cannot change font path after PlayPy23 has been initialized')
    fontPath = path

def set_audio_free(free: bool):
    global audio_free, initialized
    if initialized:
        raise InitError('Cannot change audio free status after PlayPy23 has been initialized')
    audio_free = free

def quit():
    global audio_free, initialized
    pg.quit()
    if not audio_free:
        pg.mixer.quit()
    initialized = False
    exit()

window_color = (0, 0, 0)
window_fps = 0

class window:
    '''
    Represnts a window.

    Using this class, you can create and customise a window, being able to set things like the window's title, the window's size, the window's background color, and the window's framerate.
    '''

    def __init__(
        self,
        width: int,
        height: int,
        title: str,
        color: tuple[int, int, int] = (255, 255, 255),
        fps: int = 60,
        fullscreen: bool = False,
        debug: bool = False
    ):

        global window_color
        global window_fps

        if not isinstance(width, int):
            raise TypeError(f'Provided width ({width}) is not an integer.')
        if not isinstance(height, int):
            raise TypeError(f'Provided height ({height}) is not an integer.')
        if not isinstance(title, str):
            raise TypeError(f'Provided title ({title}) is not a string.')
        if not isinstance(color, tuple):
            raise TypeError(f'Provided color ({color}) is not a tuple.')
        if not isinstance(color[0], int):
            raise TypeError(f'Provided color RED ({color[0]}) is not an integer.')
        if not isinstance(color[1], int):
            raise TypeError(f'Provided color GREEN ({color[1]}) is not an integer.')
        if not isinstance(color[2], int):
            raise TypeError(f'Provided color BLUE ({color[2]}) is not an integer.')
        if color[0] > 255 or color[0] < 0:
            raise ValueError(f'Provided color RED ({color[0]}) is out of range.')
        if color[1] > 255 or color[1] < 0:
            raise ValueError(f'Provided color GREEN ({color[1]}) is out of range.')
        if color[2] > 255 or color[2] < 0:
            raise ValueError(f'Provided color BLUE ({color[2]}) is out of range.')
        if not isinstance(fps, int):
            raise TypeError(f'Provided FPS ({fps}) is not an integer.')
        if fps < 0:
            raise ValueError(f'Provided FPS ({fps}) is out of range.')
        if not isinstance(fullscreen, bool):
            raise TypeError(f'Provided fullscreen ({fullscreen}) is not a boolean.')
        if not isinstance(debug, bool):
            raise TypeError(f'Provided debug ({debug}) is not a boolean.')

        self.width = width
        self.height = height
        self.color = color
        window_color = color
        self.title = title
        self.fullscreen = fullscreen
        self._debug = debug

        pg.display.set_caption(self.title)
        self.screen = pg.display.set_mode((self.width, self.height), pg.FULLSCREEN if self.fullscreen else 0)

        self.screen.fill(self.color)

        self.clock = pg.time.Clock()
        self.fps = fps
        window_fps = fps

        if self._debug:
            print(
                f"Window created with width {self.width}, height {self.height}, color {self.color}, title '{self.title}', FPS {self.fps}, fullscreen {self.fullscreen}, debug {self._debug}"
            )

    def tick(self, fps: int = 0):
        '''
        Ticks the window's clock.
        '''
        if fps == 0:
            fps = self.fps

        self.clock.tick(fps)
        if self._debug:
            print(f"Window ticked with FPS {fps}")

    def update(self):
        '''
        Updates the window.
        '''
        pg.display.flip()
        if self._debug:
            print("Window updated")

    def clear(self):
        '''
        Clears the window.
        '''
        self.screen.fill(self.color)
        if self._debug:
            print(f"Window cleared with color {self.color}")

    def close(self):
        '''
        Closes the window.
        '''
        pg.quit()
        if self._debug:
            print("Window closed")

    variableType = Literal['width', 'height', 'color', 'title', 'fullscreen', 'debug', 'screen', 'clock', 'fps']

    def get(self, variable: variableType):
        '''
        Gets a variable from the window.

        variable: The variable to get.
        '''
        windowvars = {
            'width': self.width,
            'height': self.height,
            'color': self.color,
            'title': self.title,
            'fullscreen': self.fullscreen,
            'debug': self._debug,
            'screen': self.screen,
            'clock': self.clock,
            'fps': self.fps
        }
        return windowvars[variable]

    def set(self, variable: variableType, value: Union[str, int, tuple[int, int, int], pg.Surface, pg.time.Clock]):
        '''
        Sets a variable from the window.

        variable: The variable to set.
        value: The value to set the variable to.
        '''

        if variable == 'width':
            if not isinstance(value, int):
                raise TypeError(f"Provided value ({value}) is not an integer.")
            if value < 0:
                raise ValueError(f"Provided value ({value}) is out of range.")
            self.width = value
            if self._debug:
                print(f"Window width set to {self.width}")
        elif variable == 'height':
            if not isinstance(value, int):
                raise TypeError(f"Provided value ({value}) is not an integer.")
            if value < 0:
                raise ValueError(f"Provided value ({value}) is out of range.")
            self.height = value
            if self._debug:
                print(f"Window height set to {self.height}")
        elif variable == 'color':
            if not isinstance(value, tuple):
                raise TypeError(f"Provided value ({value}) is not a tuple.")
            if len(value) != 3:
                raise ValueError(f"Provided value ({value}) is not a valid color.")
            if not isinstance(value[0], int):
                raise TypeError(f"Provided value RED ({value[0]}) is not an integer.")
            if not isinstance(value[1], int):
                raise TypeError(
                        f"Provided value GREEN ({value[1]}) is not an integer.")
            if not isinstance(value[2], int):
                raise TypeError(f"Provided value BLUE ({value[2]}) is not an integer.")
            if value[0] < 0 or value[0] > 255:
                raise ValueError(f"Provided value RED ({value[0]}) is out of range.")
            if value[1] < 0 or value[1] > 255:
                raise ValueError(f"Provided value GREEN ({value[1]}) is out of range.")
            if value[2] < 0 or value[2] > 255:
                raise ValueError(f"Provided value BLUE ({value[2]}) is out of range.")
            self.color = value
            if self._debug:
                print(f"Window color set to {self.color}")
        elif variable == 'title':
            if not isinstance(value, str):
                raise TypeError(f"Provided value ({value}) is not a string.")
            self.title = value
            if self._debug:
                print(f"Window title set to '{self.title}'")
        elif variable == 'fullscreen':
            if not isinstance(value, bool):
                raise TypeError(f"Provided value ({value}) is not a boolean.")
            self.fullscreen = value
            if self._debug:
                print(f"Window fullscreen set to {self.fullscreen}")
        elif variable == 'debug':
            if not isinstance(value, bool):
                raise TypeError(f"Provided value ({value}) is not a boolean.")
            self._debug = value
            if self._debug:
                print(f"Window debug set to {self._debug}")
        elif variable == 'screen':
            if not isinstance(value, pg.Surface):
                raise TypeError(f"Provided value ({value}) is not a pygame surface.")
            self.screen = value
            if self._debug:
                print(f"Window screen set to {self.screen}")
        elif variable == 'clock':
            if not isinstance(value, pg.time.Clock):
                raise TypeError(f"Provided value ({value}) is not a pygame clock.")
            self.clock = value
            if self._debug:
                print(f"Window clock set to {self.clock}")
        elif variable == 'fps':
            if not isinstance(value, int):
                raise TypeError(f"Provided value ({value}) is not an integer.")
            if value < 0:
                raise ValueError(f"Provided value ({value}) is out of range.")
            self.fps = value
            if self._debug:
                print(f"Window FPS set to {self.fps}")
        else:
            raise ValueError(
                    f"Provided variable ({variable}) is not a valid variable.")

    def set_bg(self, src: 'image | animation | pg.Surface'):
        '''
        Sets the background of the window.

        src: The source of the background.
        '''

        if not isinstance(src, (image, animation, pg.Surface)):
            raise TypeError(f"Provided source ({src}) is not a valid source.")

        self.screen.fill(self.color)

        srfc: pg.Surface | None = None
        if isinstance(src, animation):
            srfc = src.get_current_frame()
        elif isinstance(src, image):
            srfc = pg.image.load(src)
        elif isinstance(src, pg.Surface):
            srfc = src
        else:
            raise ValueError(f"Provided source ({src}) is not a valid source.")

        srfc = pg.transform.scale(srfc, (self.width, self.height))

        self.screen.blit(srfc, (0, 0))

        if self._debug:
            print(f"Window background set to {srfc}")

class eventListener:
    '''
    Finds and parses events.

    Using this class, you can find keystrokes, mouse position, and mouse clicks.
    '''

    def __init__(self, max_keys: int = 3, debug: bool = False):
        '''
        Creates an event listener.
        '''
        
        self.last_formatted = ''
        self.max_keys = max_keys
        self._debug = debug
        self.pressed_keys = []
        self.down_keys = []
        self.up_keys = []
        self.pressed_mbs = []
        self.down_mbs = []
        self.up_mbs = []
        self.quitting = False
        if self._debug:
            print(f"Event listener created with max keys {max_keys}")

    def add_events(self):
        '''
        Checks if any events have been triggered. these events include keys being pressed, mouse clicks, and window closing
        '''
        self.down_keys = []
        self.up_keys = []
        self.down_mbs = []
        self.up_mbs = []
        self.quitting = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quitting = True
            if event.type == pg.KEYDOWN:
                key = plpu.pgkeytokey[event.key]
                if key not in self.pressed_keys:
                    self.pressed_keys.append(key)
                    self.down_keys.append(key)
            if event.type == pg.KEYUP:
                key = plpu.pgkeytokey[event.key]
                if key in self.pressed_keys:
                    self.pressed_keys.remove(key)
                    self.up_keys.append(key)
            if event.type == pg.MOUSEBUTTONDOWN:
                mb = plpu.pgmbtomb[event.button]
                if mb not in self.pressed_mbs:
                    self.pressed_mbs.append(mb)
                    self.down_mbs.append(mb)
            if event.type == pg.MOUSEBUTTONUP:
                mb = plpu.pgmbtomb[event.button]
                if mb in self.pressed_mbs:
                    self.pressed_mbs.remove(mb)
                    self.up_mbs.append(mb)

    def get_if_quitting(self):
        '''
        Returns whether the window is quitting.
        '''

        return self.quitting

    def get_key_pressed(self, key: plpu.key):
        '''
        Returns whether a key is pressed or not.

        key: The key to check.
        '''
        return any(pressed_key == key for pressed_key in self.pressed_keys)

    def get_key_down(self, key: plpu.key):
        '''
        Returns whether a key is down or not.

        key: The key to check.
        '''
        return any(down_key == key for down_key in self.down_keys)

    def get_key_up(self, key: plpu.key):
        '''
        Returns whether a key is up or not.

        key: The key to check.
        '''

        return any(up_key == key for up_key in self.up_keys)

    def get_mouse_pressed(self, mb: plpu.mb):
        '''
        Returns whether a mouse button is pressed or not.

        mb: The mouse button to check.
        '''

        return any(pressed_mb == mb for pressed_mb in self.pressed_mbs)

    def get_mouse_down(self, mb: plpu.mb):
        '''
        Returns whether a mouse button is down or not.

        mb: The mouse button to check.
        '''

        return any(down_mb == mb for down_mb in self.down_mbs)

    def get_mouse_up(self, mb: plpu.mb):
        '''
        Returns whether a mouse button is up or not.

        mb: The mouse button to check.
        '''

        return any(up_mb == mb for up_mb in self.up_mbs)

    def get_pressed_keys(self, debug: Union[bool, None] = None):
        '''
        Returns the keys that are pressed.
        '''

        if debug is None:
            debug = self._debug

        formatted = ''

        if debug:
            formatted += 'all keys pressed are: '

        formatted += '<'
        formatted += ', '.join(self.pressed_keys)
        formatted += '>'

        if formatted != self.last_formatted:
            self.last_formatted = formatted
            if debug:
                print(formatted)
        if debug:
            return formatted[21:]
        return formatted

    def get_pressed_mbs(self, debug: Union[bool, None] = None):
        '''
        Returns the mouse buttons that are pressed.
        '''

        if debug is None:
            debug = self._debug

        formatted = ''

        if debug:
            formatted += 'all mouse buttons pressed are: '

        formatted += '<'
        formatted += ', '.join(self.pressed_mbs)
        formatted += '>'

        if formatted != self.last_formatted:
            self.last_formatted = formatted
            if debug:
                print(formatted)
        if debug:
            return formatted[21:]
        return formatted

    def __str__(self) -> str:
        return self.get_pressed_keys(False)

    def debug(self):
        '''
        Prints debug information if debug is enabled.
        '''

        if self._debug:
            print(f'quitting: {self.quitting}')
            self.get_pressed_keys(True)
            self.get_pressed_mbs(True)

    def set_max_keys(self, max: int = 3):
        '''
        Sets the maximum number of keys that can be pressed at once.

        max: The maximum number of keys.
        '''
        if not isinstance(max, int):
            raise TypeError(f"Provided value ({max}) is not an integer.")
        if max < 1:
            raise ValueError(f"Provided value ({max}) is out of range.")

        self.max_keys = max

    def get_max_keys(self):
        '''
        Returns the maximum number of keys that can be pressed at once.
        '''

        return self.max_keys

    def check_max_keys(self):
        '''
        Checks if the maximum number of keys has been eceeded, if it has, pop keys until the max is reached.
        '''

        if len(self.pressed_keys) > self.max_keys:
            for i in range(len(self.pressed_keys) - self.max_keys):
                self.pressed_keys.pop()


objects: list['renderer'] = []

class object:
    def __init__(
        self,
        x: int | float,
        y: int | float,
        width: int | float,
        height: int | float,
        color: tuple[int, int, int] = (0, 0, 0),
        opacity: int = 255,
        debug: bool = False,
        tag: str = ''
    ):
        '''
        Creates an object.

        ## Params:
        
        x: The x position of the object.
        y: The y position of the object.
        width: The width of the object.
        height: The height of the object.
        color: The color of the object.
        opacity: The opacity of the object.
        debug: Whether to print debug information.
        '''
        if not isinstance(x, (int, float)):
            raise TypeError(f"Provided x ({x}) is not a number.")
        if not isinstance(y, (int, float)):
            raise TypeError(f"Provided y ({y}) is not a number.")
        if not isinstance(width, (int, float)):
            raise TypeError(f"Provided width ({width}) is not a number.")
        if not isinstance(height, (int, float)):
            raise TypeError(f"Provided height ({height}) is not a number.")
        if not isinstance(color, tuple):
            raise TypeError(f"Provided color ({color}) is not a tuple.")
        if len(color) != 3:
            raise ValueError(f"Provided color ({color}) is not a valid color.")
        if not isinstance(color[0], int):
            raise TypeError(f"Provided color RED ({color[0]}) is not an integer.")
        if not isinstance(color[1], int):
            raise TypeError(f"Provided color GREEN ({color[1]}) is not an integer.")
        if not isinstance(color[2], int):
            raise TypeError(f"Provided color BLUE ({color[2]}) is not an integer.")
        if color[0] < 0 or color[0] > 255:
            raise ValueError(f"Provided color RED ({color[0]}) is out of range.")
        if color[1] < 0 or color[1] > 255:
            raise ValueError(f"Provided color GREEN ({color[1]}) is out of range.")
        if color[2] < 0 or color[2] > 255:
            raise ValueError(f"Provided color BLUE ({color[2]}) is out of range.")
        if not isinstance(opacity, int):
            raise TypeError(f"Provided opacity ({opacity}) is not an integer.")
        if opacity < 0 or opacity > 255:
            raise ValueError(f"Provided opacity ({opacity}) is out of range.")
        self.x = x
        self.y = y
        object.y = y
        self.width = width
        self.height = height
        self.color = color
        self.opacity = opacity
        self._debug = debug
        self.last_upd = ''
        self.last_drw = ''
        self.object = None
        self.surface = None
        self.tag = tag

    def update(
        self,
        x: int | float | None = None,
        y: int | float | None = None,
        width: int | float | None = None,
        height: int | float | None = None,
        color: tuple[int, int, int] | None = None,
        opacity: int | None = None,
        relative: bool = False
    ):
        '''
        Updates the object.

        ## Params:
        
        x: The x position of the object, If set to none, the object will keep its original x.
        y: The y position of the object, If set to none, the object will keep its original y.
        width: The width of the object, If set to none, the object will keep its original width.
        height: The height of the object, If set to none, the object will keep its original height.
        color: The color of the object, If set to none, the object will keep its original color.
        opacity: The opacity of the object, If set to none, the object will keep its original opacity.
        relative: Whether the values are relative to their original values.
        '''
        if x is not None:
            if relative:
                self.x += x
            else:
                self.x = x
        if y is not None:
            if relative:
                self.y += y
            else:
                self.y = y
        if width is not None:
            if relative:
                self.width += width
            else:
                self.width = width
        if height is not None:
            if relative:
                self.height += height
            else:
                self.height = height
        if color is not None:
            if relative:
                self.color += color
            else:
                self.color = color
        if opacity is not None:
            if relative:
                self.opacity += opacity
            else:
                self.opacity = opacity

        self.upd = f"Object '{self.tag}' updated with x {self.x}, y {self.y}, width {self.width}, height {self.height}, color {self.color}, opacity {self.opacity}."

        if self._debug and self.last_upd != self.upd:
            print(self.upd)
            self.last_upd = self.upd

    def create(self):
        '''
        Creates the object.
        '''

        if pg.display.get_surface() is not None:
            self.object = pg.Rect((self.x, self.y), (self.width, self.height))
            self.surface = pg.Surface((self.width, self.height))

            self.surface.fill(self.color)
            
            self.surface.set_alpha(self.opacity)

            objects.append(self)
        else:
            raise ValueError("No pygame display surface found")

    def draw(self):
        '''
        Draws the object.
        '''

        global objects

        if self.object is not None and self.surface is not None:
            pg.display.get_surface().blit(self.surface, self.object)

            self.drw = f"Object '{self.tag}' drawn with x {self.x}, y {self.y}, width {self.width}, height {self.height}, color {self.color}"

            if self._debug and self.last_drw != self.drw:
                print(self.drw)
                self.last_drw = self.drw
        else:
            raise ValueError("No object/surface found")

    def remove(self):
        '''
        Deletes the object.
        '''

        if self.object is not None:
            objects.remove(self)
        del self

    def coliding(self, other: 'renderer | pg.Rect'):
        '''
        Checks if the object is coliding with another object.

        other: The other object to check.
        '''
        
        o = other.object if isinstance(other, renderer) else other
        if self.object and o:
            return self.object.top <= o.bottom and self.object.bottom >= o.top and self.object.left <= o.right and self.object.right >= o.left
        else:
            raise ValueError("No object found")
    
    def paste(self, other: pg.Surface):
        '''
        Pastes a surface on this object.

        other: The surface to paste.
        '''

        if pg.display.get_surface() is not None:
            pg.display.get_surface().blit(other, (self.x, self.y))

class centeredobj(object):
    camera_x = 0
    camera_y = 0
    real_x = 0
    real_y = 0

    def __init__(
        self,
        x: int | float,
        y: int | float,
        width: int | float,
        height: int | float,
        color: tuple[int, int, int] = (0, 0, 0),
        opacity: int = 255,
        debug: bool = False,
        tag: str = ''
    ):
        '''
        Creates a centered object.
            
        x: The x position of the object.
        y: The y position of the object.
        width: The width of the object.
        height: The height of the object.
        color: The color of the object.
        opacity: The opacity of the object.
        debug: Whether to print debug information.
        '''

        global camera_x
        global camera_y
        global real_x
        global real_y
        
        if not isinstance(x, (int, float)):
            raise TypeError(f"Provided x ({x}) is not a number.")
        if not isinstance(y, (int, float)):
            raise TypeError(f"Provided y ({y}) is not a number.")
        if not isinstance(width, (int, float)):
            raise TypeError(f"Provided width ({width}) is not a number.")
        if not isinstance(height, (int, float)):
            raise TypeError(f"Provided height ({height}) is not a number.")
        if not isinstance(color, tuple):
            raise TypeError(f"Provided color ({color}) is not a tuple.")
        if len(color) != 3:
            raise ValueError(f"Provided color ({color}) is not a valid color.")
        if not isinstance(color[0], int):
            raise TypeError(f"Provided color RED ({color[0]}) is not an integer.")
        if not isinstance(color[1], int):
            raise TypeError(f"Provided color GREEN ({color[1]}) is not an integer.")
        if not isinstance(color[2], int):
            raise TypeError(f"Provided color BLUE ({color[2]}) is not an integer.")
        if color[0] < 0 or color[0] > 255:
            raise ValueError(f"Provided color RED ({color[0]}) is out of range.")
        if color[1] < 0 or color[1] > 255:
            raise ValueError(f"Provided color GREEN ({color[1]}) is out of range.")
        if color[2] < 0 or color[2] > 255:
            raise ValueError(f"Provided color BLUE ({color[2]}) is out of range.")
        if not isinstance(debug, bool):
            raise TypeError(f"Provided debug ({debug}) is not a boolean.")
        if not isinstance(opacity, int):
            raise TypeError(f"Provided opacity ({opacity}) is not an integer.")
        if opacity < 0 or opacity > 255:
            raise ValueError(f"Provided opacity ({opacity}) is out of range.")

        surface = pg.display.get_surface()
        screen_width = surface.get_width()
        screen_height = surface.get_height()

        self.real_x = x
        self.real_y = y
        real_x = x
        real_y = y
        self.center_x = (screen_width - width) / 2
        self.center_y = (screen_height - height) / 2
        camera_x = self.center_x
        camera_y = self.center_y
        self.width = width
        self.height = height
        self.color = color
        self.opacity = opacity
        self._debug = debug
        self.last_upd = ''
        self.last_drw = ''
        self.object = None
        self.surface = None
        self.tag = tag

    def update(
        self,
        x: int | float | None = None,
        y: int | float | None = None,
        width: int | float | None = None,
        height: int | float | None = None,
        color: tuple[int, int, int] | None = None,
        opacity: int | None = None,
        relative: bool = False
    ):
        '''
        Updates the centered object.

        x: The x position of the object, If set to none, the object will keep its original x.
        y: The y position of the object, If set to none, the object will keep its original y.
        width: The width of the object, If set to none, the object will keep its original width.
        height: The height of the object, If set to none, the object will keep its original height.
        color: The color of the object, If set to none, the object will keep its original color.
        opacity: The opacity of the object, If set to none, the object will keep its original opacity.
        relative: Whether the values are relative to their original values.
        '''

        global camera_x
        global camera_y
        global real_x
        global real_y

        surface = pg.display.get_surface()
        screen_width = surface.get_width()
        screen_height = surface.get_height()

        if x is not None:
            if relative:
                self.real_x += x
            else:
                self.real_x = x
            real_x = self.real_x
        if y is not None:
            if relative:
                self.real_y += y
            else:
                self.real_y = y
            real_y = self.real_y
        if width is not None:
            if relative:
                self.width += width
            else:
                self.width = width
            self.center_x = (screen_width - self.width) / 2
            camera_x = self.center_x
        if height is not None:
            if relative:
                self.height += height
            else:
                self.height = height
            self.center_y = (screen_height - self.height) / 2
            camera_y = self.center_y
        if color is not None:
            if relative:
                self.color += color
            else:
                self.color = color
        if opacity is not None:
            if relative:
                self.opacity += opacity
            else:
                self.opacity = opacity

        self.upd = f"Object '{self.tag}' updated with x {self.real_x}, y {self.real_y}, width {self.width}, height {self.height}, color {self.color}, opacity {self.opacity}, and was centeredd to x {self.center_x}, y {self.center_y}"

        if self._debug and self.last_upd != self.upd:
            print(self.upd)
            self.last_upd = self.upd\

    def create(self):
        '''
        Creates the centered object.
        '''

        if pg.display.get_surface() is not None:
            self.object = pg.Rect((self.center_x, self.center_y), (self.width, self.height))
            self.surface = pg.Surface((self.width, self.height))

            self.surface.fill(self.color)

            self.surface.set_alpha(self.opacity)

            objects.append(self)
        else:
            raise ValueError("No pygame display surface found")

    def draw(self):
        '''
        Draws the centered object.
        '''

        if self.object is not None and self.surface is not None:
            pg.display.get_surface().blit(self.surface, self.object)

            self.drw = f"Object '{self.tag}' drawn with x {self.real_x}, y {self.real_y}, width {self.width}, height {self.height}, color {self.color}, and was centeredd to x {self.center_x}, y {self.center_y}"

            if self._debug and self.last_drw != self.drw:
                print(self.drw)
                self.last_drw = self.drw
        else:
            raise ValueError("No object found")


class uncenteredobj(object):
    def __init__(
        self,
        x: int | float,
        y: int | float,
        width: int | float,
        height: int | float,
        color: tuple[int, int, int] = (0, 0, 0),
        opacity: int = 255,
        debug: bool = False,
        tag: str = ''
    ):
        '''
        Creates an uncentered object.

        x: The x position of the object.
        y: The y position of the object.
        width: The width of the object.
        height: The height of the object.
        color: The color of the object.
        debug: Whether to print debug information.
        '''

        global camera_x
        global camera_y
        global real_x
        global real_y

        if not isinstance(x, (int, float)):
            raise TypeError(f"Provided x ({x}) is not a number.")
        if not isinstance(y, (int, float)):
            raise TypeError(f"Provided y ({y}) is not a number.")
        if not isinstance(width, (int, float)):
            raise TypeError(f"Provided width ({width}) is not a number.")
        if not isinstance(height, (int, float)):
            raise TypeError(f"Provided height ({height}) is not a number.")
        if not isinstance(color, tuple):
            raise TypeError(f"Provided color ({color}) is not a tuple.")
        if len(color) != 3:
            raise ValueError(f"Provided color ({color}) is not a valid color.")
        if not isinstance(color[0], int):
            raise TypeError(f"Provided color RED ({color[0]}) is not an integer.")
        if not isinstance(color[1], int):
            raise TypeError(f"Provided color GREEN ({color[1]}) is not an integer.")
        if not isinstance(color[2], int):
            raise TypeError(f"Provided color BLUE ({color[2]}) is not an integer.")
        if color[0] < 0 or color[0] > 255:
            raise ValueError(f"Provided color RED ({color[0]}) is out of range.")
        if color[1] < 0 or color[1] > 255:
            raise ValueError(f"Provided color GREEN ({color[1]}) is out of range.")
        if color[2] < 0 or color[2] > 255:
            raise ValueError(f"Provided color BLUE ({color[2]}) is out of range.")
        if not isinstance(opacity, int):
            raise TypeError(f"Provided opacity ({opacity}) is not an integer.")
        if opacity < 0 or opacity > 255:
            raise ValueError(f"Provided opacity ({opacity}) is out of range.")

        self.real_x = x
        self.real_y = y
        self.center_x = x + camera_x - real_x
        self.center_y = y + camera_y - real_y
        self.width = width
        self.height = height
        self.color = color
        self.opacity = opacity
        self._debug = debug
        self.last_upd = ''
        self.last_drw = ''
        self.object = None
        self.surface = None
        self.tag = tag

    def update(
        self,
        x: int | float | None = None,
        y: int | float | None = None,
        width: int | float | None = None,
        height: int | float | None = None,
        color: tuple[int, int, int] | None = None,
        opacity: int | None = None,
        relative: bool = False
    ):
        '''
        Updates the uncentered object.

        x: The x position of the object, If set to none, the object will keep its original x.
        y: The y position of the object, If set to none, the object will keep its original y.
        width: The width of the object, If set to none, the object will keep its original width.
        height: The height of the object, If set to none, the object will keep its original height.
        color: The color of the object, If set to none, the object will keep its original color.
        opacity: The opacity of the object, If set to none, the object will keep its original opacity.
        relative: Whether the values are relative to their original values.
        '''

        global camera_x
        global camera_y
        global real_x
        global real_y

        if x is not None:
            if relative:
                self.x += x
            else:
                self.x = x
        if y is not None:
            if relative:
                self.y += y
            else:
                self.y = y
        if width is not None:
            if relative:
                self.width += width
            else:
                self.width = width
        if height is not None:
            if relative:
                self.height += height
            else:
                self.height = height
        if color is not None:
            if relative:
                self.color += color
            else:
                self.color = color
        if opacity is not None:
            if relative:
                self.opacity += opacity
            else:
                self.opacity = opacity

        self.center_x = self.real_x + camera_x - real_x
        self.center_y = self.real_y + camera_y - real_y

        self.upd = f"Object '{self.tag}' updated with x {self.real_x}, y {self.real_y}, width {self.width}, height {self.height}, color {self.color}, opacity {self.opacity}, and was centeredd to x {self.center_x}, y {self.center_y}"

        if self._debug and self.last_upd != self.upd:
            print(self.update)
            self.last_upd = self.upd

    def create(self):
        '''
        Creates the uncentered object.
        '''
        if pg.display.get_surface() is not None:
            self.object = pg.Rect((self.center_x, self.center_y), (self.width, self.height))
            self.surface = pg.Surface((self.width, self.height))

            self.surface.fill(self.color)

            self.surface.set_alpha(self.opacity)

            objects.append(self)
        else:
            raise ValueError("No pygame display surface found")

    def draw(self):
        '''
        Draws the uncentered object.
        '''

        if self.object is not None and self.surface is not None:
            pg.display.get_surface().blit(self.surface, self.object)

            self.drw = f"Object '{self.tag}' drawn with x {self.real_x}, y {self.real_y}, width {self.width}, height {self.height}, color {self.color}, and was centeredd to x {self.center_x}, y {self.center_y}"

            if self._debug and self.last_drw != self.drw:
                print(self.drw)
                self.last_drw = self.drw
        else:
            raise ValueError("No object found")

class image:
    def __init__(self, dir: str, debug: bool = False):
        '''
        Creates an image.

        dir: The directory of the image.
        debug: Whether to print debug messages.
        '''

        global imagePath

        if not isinstance(dir, str):
            raise TypeError(f"Provided directory ({dir}) is not a string.")

        dir = os.path.join(imagePath, dir)
    
        if not os.path.exists(dir):
            raise FileNotFoundError(f"Provided directory ({dir}) does not exist.")
        if not isinstance(debug, bool):
            raise TypeError(f"Provided debug ({debug}) is not a boolean.")

        self.dir = dir
        self.name = os.path.basename(dir)
        self._debug = debug
        if self._debug:
            print(f"Image '{self.name}' loaded")

    def draw(self, obj: 'renderer'):
        '''
        Draws the image.
        
        obj: The object to draw the image on.
        '''

        if not isinstance(obj, renderer):
            raise TypeError(f"Provided object ({obj}) is not a renderer.")

        obj.paste(pg.image.load(self.dir))

    def __str__(self) -> str:
        '''
        Returns the image.
        '''
        return self.dir

    def __fspath__(self) -> str:
        '''
        Returns the image.
        '''
        return os.fspath(self.dir)

class animation:
    def __init__(
        self,
        frames: list[image] | None = None,
        opacity: int = 255,
        debug: bool = False
    ):
        '''
        Creates an animation.

        frames: The frames of the animation.
        opacity: The opacity of the animation.
        debug: Whether the animation should be displayed in debug mode.
        '''
        if not isinstance(frames, list):
            raise TypeError(f"Provided frames ({frames}) is not a list.")
        if not isinstance(opacity, int):
            raise TypeError(f"Provided opacity ({opacity}) is not an integer.")
        if opacity < 0 or opacity > 255:
            raise ValueError(f"Provided opacity ({opacity}) is out of range.")
        if not isinstance(debug, bool):
            raise TypeError(f"Provided debug ({debug}) is not a boolean.")

        self.frames: list[pg.Surface] = []

        for frame in frames:
            self.frames.append(pg.image.load(frame))

        self.opacity = opacity
        self._debug = debug
        self.frame = 0
        
    def add_frames(self, *frames: image):
        '''
        Adds frames to the animation.

        frames: The frames to add.
         '''

        for frame in frames:
            if not isinstance(frame, image):
                raise TypeError(f"Provided frame ({frame}) is not an image.")
            self.frames.append(pg.image.load(frame))

    def get_frame(self, index: int | slice):
        '''
        Returns one or more frame/s of the animation.

        index: The index of the frame/s.
        '''

        if not isinstance(index, (int, slice)):
            raise TypeError(f"Provided index ({index}) is not a slice.")

        return self.frames[index]

    def get_current_frame(self):
        '''
        Returns the current frame of the animation.
        '''

        return self.frames[self.frame]

    def get_frame_count(self):
        '''
        Returns the number of frames in the animation.
        '''

        return len(self.frames)

    def suppress_obj(self, obj: 'renderer'):
        '''
        Suppresses the image to the size of an object.

        obj: The object to suppress the image to.
        '''

        if not isinstance(obj, renderer):
            raise TypeError(f"Provided obj ({obj}) is not an object.")

        for i, frame in enumerate(self.frames):
            self.frames[i] = pg.transform.scale(frame, (obj.width, obj.height))
            if self._debug:
                print(f"Frame {frame} suppressed to size {obj.width}×{obj.height}")

    def suppress(self, width: int, height: int):
        '''
        Suppresses the image to the size of a width and height.

        width: The width to suppress the image to.
        height: The height to suppress the image to.
        '''

        for i, frame in enumerate(self.frames):
            self.frames[i] = pg.transform.scale(frame, (width, height))
            if self._debug:
                print(f"Frame {i} suppressed to width {width} and height {height}")

    def next_frame(self):
        '''
        Goes to the next frame of the animation.
        '''

        self.frame += 1
        if self.frame >= len(self.frames):
            self.frame = 0

    def set_frame(self, index: int):
        '''
        Sets the frame of the animation.

        index: The index of the frame.
        '''

        if not isinstance(index, int):
            raise TypeError(f"Provided index ({index}) is not an integer.")

    def draw(self, obj: 'renderer'):
        '''
        Draws the current frame.

        obj: The object to draw the frame to.
        '''

        if not isinstance(obj, renderer):
            raise TypeError(f"Provided obj ({obj}) is not an object.")

        img = self.frames[self.frame]
        img.set_alpha(self.opacity)
        
        obj.paste(img)

    def __str__(self) -> str:
        '''
        Returns the animation.
        '''
        formatted = '/'
        for frame in self.frames:
            formatted += f"{frame}, "
        formatted = formatted[:-2]
        formatted += '\\'
        return formatted

    def __getitem__(self, index: int | slice):
        '''
        Returns one or more frame/s of the animation.

        index: The index of the frame/s.
        '''
        if not isinstance(index, (int, slice)):
            raise TypeError(f"Provided index ({index}) is not a slice.")

        return self.frames[index]

    def __setitem__(self, index: int, value: image):
        '''
        Sets a frame of the animation.

        index: The index of the frame.
        value: The value to set.
        '''

        if not isinstance(index, int):
            raise TypeError(f"Provided index ({index}) is not an integer.")
        if not isinstance(value, image):
            raise TypeError(f"Provided value ({value}) is not an image or a list of images.")

        self.frames[index] = pg.image.load(value)

    def __delitem__(self, index: int | slice):
        '''
        Deletes one or more frame/s of the animation.

        index: The index of the frame/s.
        '''

        if not isinstance(index, (int, slice)):
            raise TypeError(f"Provided index ({index}) is not a slice.")
            
        del self.frames[index]

    def __len__(self):
        '''
        Returns the number of frames in the animation.
        '''

        return len(self.frames)

    def __iter__(self):
        '''
        Returns the frames of the animation.
        '''

        return iter(self.frames)

class text:
    def __init__(
        self,
        text: str,
        font_path: str,
        size: int,
        color: tuple[int, int, int] = (0, 0, 0),
        opacity: int = 255,
        debug: bool = False
    ):
        '''
        Creates a text object.

        text: The text to display.
        font_path: The path of the font to use.
        size: The size of the text.
        color: The color of the text.
        debug: Whether to print debug messages.
        '''

        global fontPath

        if not isinstance(text, str):
            raise TypeError(f"Provided text ({text}) is not a string.")
        if not isinstance(font_path, str):
            raise TypeError(f"Provided font_path ({font_path}) is not a string.")

        font_path = os.path.join(fontPath, font_path)
    
        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Provided font_path ({font_path}) does not exist.")
        if not isinstance(size, int):
            raise TypeError(f"Provided size ({size}) is not an integer.")
        if not isinstance(color, tuple):
            raise TypeError(f"Provided color ({color}) is not a tuple.")
        if not isinstance(opacity, int):
            raise TypeError(f"Provided opacity ({opacity}) is not an integer.")
        if not isinstance(debug, bool):
            raise TypeError(f"Provided debug ({debug}) is not a boolean.")

        self.text = text
        self.path = font_path
        self.font = pg.font.Font(font_path, size)
        self.color = color
        self.opacity = opacity
        self._debug = debug
        
        if self._debug:
            print(f"Text '{self.text}' loaded")

    def update(self, text: str):
        '''
        Updates the text.
        
        text: The new text.
        '''

        if not isinstance(text, str):
            raise TypeError(f"Provided text ({text}) is not a string.")

        self.text = text

    anchor_point = Literal[
        'topleft', 'topcenter', 'topright',
        'centerleft', 'center', 'centerright',
        'bottomleft', 'bottomcenter', 'bottomright'
    ]
    def draw(self, pos: tuple[int, int], anchor: anchor_point, antialias: bool = True):
        '''
        Draws the text.

        pos: The position of the text.
        anchor: The anchor point of the text.
        '''

        if not isinstance(pos, tuple):
            raise TypeError(f"Provided pos ({pos}) is not a tuple.")
        if not isinstance(anchor, str):
            raise TypeError(f"Provided anchor ({anchor}) is not a string.")
        if anchor not in ['topleft', 'topcenter', 'topright', 'centerleft', 'center', 'centerright', 'bottomleft', 'bottomcenter', 'bottomright']:
            raise ValueError(f"Provided anchor ({anchor}) is not a valid anchor point.")
        if not isinstance(antialias, bool):
            raise TypeError(f"Provided antialias ({antialias}) is not a boolean value.")
        t = self.font.render(self.text, antialias, self.color)
        t.set_alpha(self.opacity)
        t_rect = t.get_rect()
        if anchor == 'topleft':
            t_rect.topleft = pos
        elif anchor == 'topcenter':
            t_rect.midtop = pos
        elif anchor == 'topright':
            t_rect.topright = pos
        elif anchor == 'centerleft':
            t_rect.midleft = pos
        elif anchor == 'center':
            t_rect.center = pos
        elif anchor == 'centerright':
            t_rect.midright = pos
        elif anchor == 'bottomleft':
            t_rect.bottomleft = pos
        elif anchor == 'bottomcenter':
            t_rect.midbottom = pos
        elif anchor == 'bottomright':
            t_rect.bottomright = pos
            
        pg.display.get_surface().blit(t, t_rect)

        if self._debug:
            print(f"Text '{self.text}' drawn at {pos} with anchor '{anchor}'")

    def __str__(self) -> str:
        '''
        Returns the text.
        '''

        return self.text

    def __fspath__(self):
        '''
        Returns the path of the font.
        '''

        return self.path

class sound:
    def __init__(
        self,
        path: str,
        channel: int = 0,
        loop: bool = False,
        debug: bool = False
    ):
        '''
        Creates a sound object.

        ## Params:

        path: The path of the sound to play.
        channel: The channel to play the sound on.
        loop: Whether to loop the sound.
        debug: Whether to print debug messages.
        '''

        global soundPath, audio_free

        if audio_free:
            raise RuntimeError("Audio is not available.")

        if not isinstance(path, str):
            raise TypeError(f"Provided path ({path}) is not a string.")

        path = os.path.join(soundPath, path)
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"Provided path ({path}) does not exist.")
        if not isinstance(loop, bool):
            raise TypeError(f"Provided loop ({loop}) is not a boolean value.")
        if not isinstance(debug, bool):
            raise TypeError(f"Provided debug ({debug}) is not a boolean value.")

        self.path = path
        self.sound = pg.mixer.Sound(path)
        self.channel = pg.mixer.Channel(channel)
        self.loop = loop
        self._debug = debug

        if self._debug:
            print(f"Sound '{path}' loaded")

    def play(self):
        '''
        Plays the sound.
        '''

        self.channel.play(self.sound, loops=self.loop)

        if self._debug:
            print(f"Sound '{self.path}' played")

    def stop(self):
        '''
        Stops the sound.
        '''

        self.channel.stop()

        if self._debug:
            print(f"Sound '{self.path}' stopped")

    def pause(self):
        '''
        Pauses the sound.
        '''

        self.channel.pause()

        if self._debug:
            print(f"Sound '{self.path}' paused")

    def resume(self):
        '''
        Resumes the sound.
        '''

        self.channel.unpause()

        if self._debug:
            print(f"Sound '{self.path}' resumed")

    def update(self, path: str):
        '''
        Updates the sound.

        ## Params:

        path: The new path of the sound.
        '''

        global soundPath
        
        if not isinstance(path, str):
            raise TypeError(f"Provided path ({path}) is not a string.")

        path = os.path.join(soundPath, path)
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"Provided path ({path}) does not exist.")

        self.path = path
        self.sound = pg.mixer.Sound(path)

        if self._debug:
            print(f"Sound '{self.path}' updated")

    def __str__(self) -> str:
        '''
        Returns the sound.
        '''

        return self.path

    def __fspath__(self):
        '''
        Returns the path representation of the sound.
        '''

        return self.path

def clip(obj1: 'renderer', obj2: 'renderer | pg.Rect'):
    '''
    Gets which side `obj1` is coliding with `obj2` on, and clips `obj1` to that side of `obj2`.

    ## Params:

    obj1: The object to clip.
    obj2: The object to clip `obj1` to.

    ## Returns:

    int: The side of `obj2` that `obj1` is coliding with. 0 means no collision, 1 means colliding on the left, 2 means colliding on the right, 3 means colliding on the top, and 4 means colliding on the bottom.
    '''

    if not isinstance(obj1, renderer):
        raise TypeError(f"Provided obj1 ({obj1}) is not a renderer.")
    if not isinstance(obj2, (renderer, pg.Rect)):
        raise TypeError(f"Provided obj2 ({obj2}) is not a renderer.")

    if obj1.coliding(obj2):
        clipleftx = obj2.x - obj1.width
        clipleftdist = abs(obj1.x - clipleftx)
        cliprightx = obj2.x + obj2.width
        cliprightdist = abs(obj1.x - cliprightx)
        clipupy = obj2.y - obj1.height
        clipupdist = abs(obj1.y - clipupy)
        clipdowny = obj2.y + obj2.height
        clipdowndist = abs(obj1.y - clipdowny)
        dists = (clipleftdist, cliprightdist, clipupdist, clipdowndist)
        if min(dists) == clipleftdist:
            obj1.x = clipleftx
            return 1
        elif min(dists) == cliprightdist:
            obj1.x = cliprightx
            return 2
        elif min(dists) == clipupdist:
            obj1.y = clipupy
            return 3
        elif min(dists) == clipdowndist:
            obj1.y = clipdowny
            return 4
    else:
        return 0

class physicsindex:
    def __init__(
        self,
        x: int | float,
        y: int | float,
        width: int | float,
        height: int | float,
        xvel: int | float = 0,
        yvel: int | float = 0,
        collidable: bool = True,
        grav_enabled: bool = False,
        gravity: float = 0.5,
    ):
        '''
        Creates a physics index.

        ## Params:

        x: The x position of the physics index.
        y: The y position of the physics index.
        width: The width of the physics index.
        height: The height of the physics index.
        xvel: The x velocity of the physics index.
        yvel: The y velocity of the physics index.
        collidable: Whether the physics index is collidable or not.
        friction: The friction of the physics index.
        grav_enabled: Whether the physics index has gravity or not.
        gravity: The gravity of the physics index.
        '''
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.xvel = xvel
        self.yvel = yvel
        self.collidable = collidable
        self.grav_enabled = grav_enabled
        self.gravity = gravity
        self.__index = (self.x, self.y, self.width, self.height, self.xvel, self.yvel, self.collidable, self.grav_enabled, self.gravity)

    def get_index(self):
        '''
        Returns the physics index.
        '''
        return self.__index

    def __getitem__ (self, index: slice):
        '''
        Returns a slice of the physics index.

        index: The index to get.
        '''

        return self.__index[index]

class physicsobj(object):
    def __init__(
        self,
        x: int | float,
        y: int | float,
        width: int | float,
        height: int | float,
        color: tuple[int, int, int] = (0, 0, 0),
        opacity: int = 255,
        colisions_enabled: bool = True,
        gravity_enabled: bool = False,
        gravity: float = 0.5,
        jump_force: float = 10,
        max_jumps: int = 2,
        debug: bool = False,
        tag: str = ''
    ):
        '''
        Creates a physics object.

        ## Params:

        x: The x position of the object.
        y: The y position of the object.
        width: The width of the object.
        height: The height of the object.
        color: The color of the object.
        opacity: The opacity of the object.
        colisions_enabled: Whether the object should be able to collide with other objects.
        gravity_enabled: Whether the object should be able to have gravity.
        gravity: The gravity of the object (if gravity is enabled).
        jump_force: The force of the object's jump (if gravity is enabled).
        debug: Whether the object should be debugged.
        '''
        if not isinstance(x, (int, float)):
            raise TypeError(f"Provided x ({x}) is not a number.")
        if not isinstance(y, (int, float)):
            raise TypeError(f"Provided y ({y}) is not a number.")
        if not isinstance(width, (int, float)):
            raise TypeError(f"Provided width ({width}) is not a number.")
        if not isinstance(height, (int, float)):
            raise TypeError(f"Provided height ({height}) is not a number.")
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.opacity = opacity
        self.vx = 0
        self.vy = 0
        self.mx = False
        self.my = False
        self.colisions_enabled = colisions_enabled
        self.gravity_enabled = gravity_enabled
        self.gravity = gravity
        self.jump_force = jump_force
        self.max_jumps = max_jumps
        self.jump_count = 0
        self.jumping = False
        self.correct_order = False
        self.object = None
        self.last_drw = ''
        self._debug = debug
        self.tag = tag

    def jump(self):
        '''
        Makes the object jump.
        '''
        self.jumping = True

    def update(
        self,
        x: int | float | None = None,
        y: int | float | None = None,
        width: int | float | None = None,
        height: int | float | None = None,
        color: tuple[int, int, int] | None = None,
        opacity: int | float | None = None,
        colisions_enabled: bool | None = None,
        gravity_enabled: bool | None = None,
        gravity: float | None = None,
        jump_force: float | None = None,
        max_jumps: int | None = None,
        relative: bool = False,
    ):
        '''
        Updates the object.

        ## Params:

        x: The x position of the object.
        y: The y position of the object.
        width: The width of the object.
        height: The height of the object.
        color: The color of the object.
        opacity: The opacity of the object.
        colisions_enabled: Whether the object should be able to collide with other objects.
        gravity_enabled: Whether the object should be able to have gravity.
        gravity: The gravity of the object (if gravity is enabled).
        jump_force: The force of the object's jump (if gravity is enabled).
        max_jumps: The maximum number of jumps the object can have.
        relative: Whether the values should be relative to their original values.
        '''
        if x is not None:
            if relative:
                self.x += x
            else:
                self.x = x
        if y is not None:
            if relative:
                self.y += y
            else:
                self.y = y
        if width is not None:
            if relative:
                self.width += width
            else:
                self.width = width
        if height is not None:
            if relative:
                self.height += height
            else:
                self.height = height
        if color is not None:
            if relative:
                self.color += color
            else:
                self.color = color
        if opacity is not None:
            if relative:
                self.opacity += opacity
            else:
                self.opacity = opacity
        if colisions_enabled is not None:
            self.colisions_enabled = colisions_enabled
        if gravity_enabled is not None:
            self.gravity_enabled = gravity_enabled
        if gravity is not None:
            if relative:
                self.gravity += gravity
            else:
                self.gravity = gravity
        if jump_force is not None:
            if relative:
                self.jump_force += jump_force
            else:
                self.jump_force = jump_force
        if max_jumps is not None:
            if relative:
                self.max_jumps += max_jumps
            else:
                self.max_jumps = max_jumps

        if self._debug:
            print(f"Object updated: {self}")

    def update_velocity(
        self,
        x: int | float | None = None,
        y: int | float | None = None
    ):
        '''
        Updates the object's velocity.

        ## Params:

        x: The x velocity of the object.
        y: The y velocity of the object.
        '''

        if x is not None:
            if self.mx:
                self.vx += x
            else:
                self.vx = x
                self.mx = True
        if y is not None:
            if self.my:
                self.vy += y
            else:
                self.vy = y
                self.my = True
        if self._debug:
            print(f"Object velocity updated: {self}")

    def apply_force(
        self,
        x: int | float = 0,
        y: int | float = 0
    ):
        '''
        Applies a force to the object.

        ## Params:

        x: The x force to apply.
        y: The y force to apply.
        '''

        self.vx += x
        self.vy += y

    def create(self):
        self.correct_order = True
        return super().create()

    def draw(self):
        self.correct_order = False
        return super().draw()

    def physics_update(self):
        '''
        Updates the object based on its physics.

        ## Returns:

        physicsindex: The object's physics index.
        '''

        if not self.correct_order:
            raise ValueError("Physics update must be called between object creation and object drawing.")
        if self._debug:
            print(f'Object before update: {self}')
        c = False
        if self.colisions_enabled:
            for obj in objects:
                if obj != self:
                    col = clip(self, obj)
                    if col != 0 and self._debug:
                        print(f'Object colliding with {obj} on side {col}, updated object: {self}')
                    if col in [1, 2]:
                        self.vx = min(self.vx, 0) if col == 1 else max(self.vx, 0)
                        if self._debug:
                            print(f'Object friction applied: {self}')
                    if col == 3 and self.gravity_enabled:
                        self.jump_count = 0
                    if col in [3, 4]:
                        self.vy = min(self.vy, 0) if col == 3 else max(self.vy, 0)
                        c = col == 3
                        if self._debug:
                            print(f'Object friction applied: {self}')
        if self.jump_count < self.max_jumps and self.gravity_enabled and self.jumping:
            self.vy = -self.jump_force
            self.jump_count += 1
            c = True
            if self._debug:
                print(f'Object jump applied: {self}')
        if self.gravity_enabled and not c:
            self.vy += self.gravity
            if self._debug:
                print(f'Object gravity applied: {self}')
        self.x += self.vx
        self.y += self.vy
        self.jumping = False
        self.mx = False
        self.my = False
        if self._debug:
            print(f"Object physics updated: {self}")
        return get_physics_index(self)

    def __str__(self) -> str:
        '''
        Returns the object's string.
        '''

        return f"Object: '{self.tag}' | X: {self.x} | Y: {self.y} | Width: {self.width} | Height: {self.height} | Color: {self.color} | Velocity X: {self.vx} | Velocity Y: {self.vy} | Collision Enabled: {self.colisions_enabled} | Gravity Enabled: {self.gravity_enabled} | Gravity: {self.gravity} | Jump Force: {self.jump_force} | Max Jumps: {self.max_jumps} | Jump Count: {self.jump_count}"

def get_physics_index(obj: 'physicsobj'):
    '''
    Gets the physics index of an object.

    obj: The object to get the physics index of.
    '''

    return physicsindex(obj.x, obj.y, obj.width, obj.height, obj.vx, obj.vy, obj.colisions_enabled, obj.gravity_enabled, obj.gravity)

renderer = object | centeredobj | uncenteredobj | physicsobj