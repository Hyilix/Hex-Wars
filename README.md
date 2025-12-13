Hex-Wars
========

https://github.com/Hyilix/Hex-Wars

Team:
* Ursescu Sebastian https://github.com/Hyilix - 325 CA -> Project "Leader" (the one who sent the assignments to moodle)
* Stoian Andrei-Alexandru https://github.com/Frasdemsky - 331 CD 

Made entirely in Python (using primarily Pygame).

Made for the project assignment for university course IA4 (2025).

> Feel free to use and modify to your heart's content

# Description

Hex-Wars is a 2D top-down turn-based strategy game where the players fight for being the last on the map.

Each player has control over the map by controlling the hexes. To gain control of a hex, move a unit onto the corresponding hex. However, units and towers can protect adjacent hexes from attacks by enemy units.

A core aspect of the game involves the economy management. Each tile controlled by a player grants him +1 income. Additionally, the player can buy farms on a controlled hex to increase the income with +4 per farm.
Each unit and tower costs income, and when the income is negative, the state reserved begins to deplete. When the money reaches 0, all units will die, freeing the income consumed.

The strategic depth of this game comes from the mechanic that a territory controlled by a player can be cut, each half working as an independent state, with its separate income and reserve.
Cutting off an expensive army into a poor region will ensure that that army will starve, allowing for a tempo to gain ground or reinforce the defences.

The game is simple in its design. It takes the approach of "easy to learn - hard to master".

The game also features a map editor, where new maps can be created, or existing ones can be modified.

Each action can be undone or redone, so there is no penalty of doing a mistake on your turn. This works in the editor, too.

It is heavily inspired by Antiyoy (by Yiotro) and Slay (by Sean O'Connor).

# How to run

To run the game, open the `src/` directory and type `python main.py`. Python version 3.* is expected to be install in order to run the game.

The screen size can be modified by changing the `screen_size` variable inside of `main.py`. Since the game is made using python, there is no need for recompiling the game after making a change.

The game has a variety of controls. In the editor, pressing `CTRL + h` will pop up a screen with all the commands available.

To undo/redo an action, press `CTRL + z`/`CTRL + y` respectivelly.

To save/load a map (inside the editor), press `CTRL + s`/`CTRL + l` respectivelly.

# Modifying the game

As stated above, you can **Feel free to use and modify to your hearts content**. The game is easily configurable.

One way to modify the game is by modifying the `colors.py` file to add/remove/change any colors in-game. Simply add any colors of your choosing, and a player can use that color by adding it into the `available_colors` list.

# Technologies used

This game was made entirely in Python. That said, some packages were used in the making of this game:
* pygame: https://github.com/Hyilix/Hex-Wars A wrapper over SDL 2.0 for handling rendering, audio, input and events. The core essentials of a game. Used almost everywhere. 
* pickle: https://docs.python.org/3/library/pickle.html A library used in serialization and deserialization of python object. Used in serializing and unserializing the maps (saving/loading)

# Team workload

Each member contributed to the project as follows:
* Ursescu Sebastian - 325 CA: Rendering system, Editor system, Map serialization, Menu system, Mouse/Keyboard handling, Lobby system, Gameplay system, Player and Territory handling, Game assets, Readme file.
* Stoian Andrei-Alexandru - 331 CD: Colors, Button system, Prototyping the main class and the event handler, Player handling and unit moving prototypes.

# Difficulties encountered

Having a project of this size, there are bound to be some issues. Here's a small breakdown of them:

- The handling of territory. A player can have independent regions of territory that are controlled each turn. To solve this, the state system was built,
where the player controls state entities that themselves hold the hexes controlled, the income and the money
- The action handler (undo/redo system) would incorrectly interact with the state system. To solve this, each hex that has been actioned to will be rerun through the state handling algorithm
- The button system. You may want a simple button, or a button with a texture, or a slider button (this is present in the editor to control the brush size).
To solve this, a main Button class was implemented, alongside child implementations of the button. Standard OOP phylosophy.
- Different colored hexes. The player can have any color they wish for the hexes. To make a separate sprite for the hex for each color is inefficient.
To solve this, a single tile sprite is present, and the game renderer will create a template of the colored hex to use on demand. It doesn't generate all possible colors variations, only what is necessary.
- Handling big maps. The map cannot be only one surface. Zooming in/out of it would be a nightmare and would bring the system to a halt on big maps. To solve this, the map is split into chunks of surfaces
and drawn on demand. Simillar to the minecraft chunks system, only that in this project is used only for rendering.

# Afterthougths

Altough a really fun project to work on, we greatly underestimated the time and effort it took to finalize this project. Still, this proved to be a good exercise in implementing a real python application. 
What we tried to achieve is a lightweight, and modular game. We partlty achieved this, the overlooked areas being serialized game parameters (that could be stored inside a .yaml file for example),
and the button system is quite limited in the tasks that it can do. Still, there are also great aspects, such as the game renderer, that despite the several optimisations lacking for a smoother experience,
can theoretically handle and render infinite maps, due to the rendering of chunks only visible to the screen. Definetely, a part of the project with the most work put into it.

The map editor is a part of the project that we can be proud of. Featuring pen, fill mode, brush size and various options to draw, alongside the action handler for undo/redo the tile placement,
the editor provides a way to create any playable map with ease. 
