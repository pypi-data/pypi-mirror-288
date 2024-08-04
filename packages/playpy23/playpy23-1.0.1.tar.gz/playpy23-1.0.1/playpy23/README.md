# PlayPy23

pygame is an amazing library, but it is very complex, with making full games needing a lot of experience, so i made PlayPy23. PlayPy23 is a beginner friendly python library for making games. It is written on top of the pygame library, and with it you can create fully functional games in a matter of seconds. Like pygame, it is highly portable and customizable.

> Note: PlayPy23 is abbreviated 'plp'

## Installation

To install PlayPy23, just type the following command to your terminal

```bash
pip install PlayPy23
```

## Usage

To use PlayPy23, there are a couple of initialization options and steps you must follow, they include:  

1. PlayPy23 has built in `imagePath`, `soundPath`, and `fontPath` directory variables that must have their respective directories created pre-init, they default to `'assets/images'`, `'assets/sounds'`, and `'assets/fonts'`, but they can be changed using the `set_image_path()`, `set_sound_path()`, and `set_font_path()` functions.
2. PlayPy23 also has an `audio_free` variable (defaults to `False`) that can be changed using the `set_audio_free()` function.
3. PlayPy23 has `init()` and `quit()` functions that initialize and quit out of PlayPy23, initialization options cannot be set between the `init()` and `quit()` functions, and things like object creation, and the game loop must be created between the functions.

## Documentation

There is no PlayPy23 documentation, yet...

## Community

Join the PlayPy23 Discord server [here](https://discord.gg/XnRKWwMKBk) to connect with other users, get help, and share your projects!

## License

PlayPy23 is licensed under the GNU General Public License. See the `LICENSE` file for more details