import pygame

import Events
import button
import Doodads
import GameHandler
import Menu

DEFAULT_UI_PATH = "../assets/ui/editor/"
DEFAULT_UI_LOBBY_PATH = "../assets/ui/lobby/"

# Button functions
# Main buttons
def open_menu(editor, button):
    GameHandler.GameHandler().switch_tab(GameHandler.CurrentTab.MAINMENU)

# def select_picker(editor, button):
#     deselect_all(editor.utiltab)
#     select_this(button)

def select_fill(editor, button):
    deselect_all(editor.utiltab)
    select_this(button)
    editor.set_fill(True)

def select_undo(editor, button):
    editor.handle_action_handler(True)

def select_redo(editor, button):
    editor.handle_action_handler(False)

def select_pen(editor, button):
    deselect_all(editor.utiltab)
    select_this(button)
    editor.set_fill(False)

def change_brush(editor, button):
    min_brush = 1
    max_brush = 10

    brush = min_brush + int(button.slider_progress / 100 * (max_brush - min_brush))

    first, second = button.content.split(':')
    button.content = first + ": " + str(brush)

    editor.brush.change_size(brush)

def center_world(editor, button):
    pygame.event.post(pygame.event.Event(Events.CENTER_CAMERA))

# Main Menu buttons
def switch_to_editor(game_handler, button):
    game_handler.switch_tab(GameHandler.CurrentTab.EDITOR)

def switch_to_lobby(game_handler, button):
    game_handler.switch_tab(GameHandler.CurrentTab.LOBBY)

def quit_game(game_handler, button):
    game_handler.stop_game()

# Lobby buttons
def player_color_hex(game_handler, button):
    game_handler.lobby_change_color(button)

def player_join(game_handler, button):
    game_handler.lobby_join_player()

def player_leave(game_handler, button):
    game_handler.lobby_remove_player(button)

def lobby_start(game_handler, button):
    game_handler.lobby_get_color_scheme()

    if game_handler.lobby_found_map():
        game_handler.switch_tab(GameHandler.CurrentTab.MAPPICKER)
    else:
        print("No maps for the current configuration found")

def lobby_back_to_menu(game_handler, button):
    game_handler.switch_tab(GameHandler.CurrentTab.MAINMENU)

# World buttons
def select_owner_no(editor, button):
    select_owner(editor, button)
    editor.change_owner(-1)

def select_owner0(editor, button):
    select_owner(editor, button)
    editor.change_owner(0)

def select_owner1(editor, button):
    select_owner(editor, button)
    editor.change_owner(1)

def select_owner2(editor, button):
    select_owner(editor, button)
    editor.change_owner(2)

def select_owner3(editor, button):
    select_owner(editor, button)
    editor.change_owner(3)

def select_owner4(editor, button):
    select_owner(editor, button)
    editor.change_owner(4)

def select_owner5(editor, button):
    select_owner(editor, button)
    editor.change_owner(5)

def select_owner6(editor, button):
    select_owner(editor, button)
    editor.change_owner(6)

def select_doodad_no(editor, button):
    select_doodad(editor, button)
    editor.change_doodad(None)

def select_doodad_unit1(editor, button):
    select_doodad(editor, button)
    editor.change_doodad(Doodads.UnitTier1(0))

def select_doodad_unit2(editor, button):
    select_doodad(editor, button)
    editor.change_doodad(Doodads.UnitTier2(0))

def select_doodad_unit3(editor, button):
    select_doodad(editor, button)
    editor.change_doodad(Doodads.UnitTier3(0))

def select_doodad_unit4(editor, button):
    select_doodad(editor, button)
    editor.change_doodad(Doodads.UnitTier4(0))

def select_doodad_tower1(editor, button):
    select_doodad(editor, button)
    editor.change_doodad(Doodads.TowerTier1(0))

def select_doodad_tower2(editor, button):
    select_doodad(editor, button)
    editor.change_doodad(Doodads.TowerTier2(0))

def select_doodad_base(editor, button):
    select_doodad(editor, button)
    editor.change_doodad(Doodads.TownCenter(0))

def select_doodad_farm(editor, button):
    select_doodad(editor, button)
    editor.change_doodad(Doodads.Farm(0))

def select_doodad_tree(editor, button):
    select_doodad(editor, button)
    editor.change_doodad(Doodads.Tree())

def select_doodad_grave(editor, button):
    select_doodad(editor, button)
    editor.change_doodad(Doodads.Grave())

# Auxiliary functions
def select_doodad(editor, button):
    deselect_doodads(editor.worldtab)
    select_this(button)

def select_owner(editor, button):
    deselect_owners(editor.worldtab)
    select_this(button)

def deselect_all(tab):
    for button in tab.get_buttons():
        if button.is_highlighted:
            button.set_highlight(False)

def deselect_owners(tab):
    for button in tab.get_buttons():
        if button.is_doodad() == False:
            button.set_highlight(False)

def deselect_doodads(tab):
    for button in tab.get_buttons():
        if button.is_doodad() == True:
            button.set_highlight(False)

def select_this(button):
    button.set_highlight(True)

# Map picker buttons
def switch_to_gameplay(game_handler, button):
    game_handler.set_map_to_load(button.get_str_data())
    game_handler.switch_tab(GameHandler.CurrentTab.GAMEPLAY)

# Loader functions
def load_main_buttons():
    buttons : list[button.TextureButton] = []

    menu = button.TextureButton((0, 0), (64, 64), open_menu)
    menu.load_texture(DEFAULT_UI_PATH + "main/Menu Button.png")
    buttons.append(menu)

    # picker = button.TextureButton((0, 0), (64, 64), select_picker)
    # picker.load_texture(DEFAULT_UI_PATH + "main/Picker.png")
    # buttons.append(picker)

    fill = button.TextureButton((0, 0), (64, 64), select_fill)
    fill.load_texture(DEFAULT_UI_PATH + "main/Fill.png")
    buttons.append(fill)

    pen = button.TextureButton((0, 0), (64, 64), select_pen)
    pen.load_texture(DEFAULT_UI_PATH + "main/Pen.png")
    pen.set_highlight(True)
    buttons.append(pen)

    undo = button.TextureButton((0, 0), (64, 64), select_undo)
    undo.load_texture(DEFAULT_UI_PATH + "main/Undo.png")
    buttons.append(undo)

    redo = button.TextureButton((0, 0), (64, 64), select_redo)
    redo.load_texture(DEFAULT_UI_PATH + "main/Redo.png")
    buttons.append(redo)

    return buttons

def load_misc_buttons():
    buttons : list[button.Button] = []

    center = button.TextureButton((0, 0), (196, 64), center_world)
    center.load_texture(DEFAULT_UI_PATH + "center/Center.png")
    buttons.append(center)

    brush = button.SliderButton((0, 0), (196, 64), "Brush: 1", change_brush)
    buttons.append(brush)

    return buttons

def load_menu_buttons():
    buttons : list[button.SimpleButton] = []

    lobby = button.SimpleButton((0, 0), (512, 128), "Lobby", switch_to_lobby)
    buttons.append(lobby)

    editor = button.SimpleButton((0, 0), (512, 128), "Editor", switch_to_editor)
    buttons.append(editor)

    quit_button = button.SimpleButton((0, 0), (512, 128), "Quit Game", quit_game)
    buttons.append(quit_button)

    return buttons

def load_lobby_hexes():
    buttons : list[button.Button] = []

    hex1 = button.TextureButton((0, 0), (128, 128), player_color_hex)
    hex1.load_texture(DEFAULT_UI_LOBBY_PATH + "HexTile.png")
    buttons.append(hex1)

    hex2 = button.TextureButton((0, 0), (128, 128), player_color_hex)
    hex2.load_texture(DEFAULT_UI_LOBBY_PATH + "HexTile.png")
    buttons.append(hex2)

    hex3 = button.TextureButton((0, 0), (128, 128), player_color_hex)
    hex3.load_texture(DEFAULT_UI_LOBBY_PATH + "HexTile.png")
    buttons.append(hex3)

    hex4 = button.TextureButton((0, 0), (128, 128), player_color_hex)
    hex4.load_texture(DEFAULT_UI_LOBBY_PATH + "HexTile.png")
    buttons.append(hex4)

    hex5 = button.TextureButton((0, 0), (128, 128), player_color_hex)
    hex5.load_texture(DEFAULT_UI_LOBBY_PATH + "HexTile.png")
    buttons.append(hex5)

    hex6 = button.TextureButton((0, 0), (128, 128), player_color_hex)
    hex6.load_texture(DEFAULT_UI_LOBBY_PATH + "HexTile.png")
    buttons.append(hex6)

    return buttons

def load_lobby_buttons():
    screen_size = GameHandler.GameHandler().get_screen().get_size()

    buttons : list[button.Button] = []

    main_menu = button.SimpleButton((screen_size[0] // 30, screen_size[1] // 30), (128, 64), "Main Menu", lobby_back_to_menu)
    main_menu.change_font(20)
    buttons.append(main_menu)

    start = button.SimpleButton((screen_size[0] // 2 - 64, screen_size[1] // 10 * 8), (128, 64), "Start", lobby_start)
    start.change_font(20)
    buttons.append(start)

    return buttons

def load_lobby_join_buttons():
    buttons : list[button.SimpleButton] = []

    join = button.SimpleButton((0, 0), (128, 48), "Join", player_join)
    join.change_font(18)
    buttons.append(join)

    return buttons

def load_lobby_leave_buttons():
    buttons : list[button.SimpleButton] = []

    leave1 = button.SimpleButton((0, 0), (128, 48), "Leave", player_leave)
    leave1.change_font(18)
    leave1.active = False
    buttons.append(leave1)

    leave2 = button.SimpleButton((0, 0), (128, 48), "Leave", player_leave)
    leave2.change_font(18)
    leave2.active = False
    buttons.append(leave2)

    leave3 = button.SimpleButton((0, 0), (128, 48), "Leave", player_leave)
    leave3.change_font(18)
    leave3.active = False
    buttons.append(leave3)

    leave4 = button.SimpleButton((0, 0), (128, 48), "Leave", player_leave)
    leave4.change_font(18)
    leave4.active = False
    buttons.append(leave4)

    leave5 = button.SimpleButton((0, 0), (128, 48), "Leave", player_leave)
    leave5.change_font(18)
    leave5.active = False
    buttons.append(leave5)

    leave6 = button.SimpleButton((0, 0), (128, 48), "Leave", player_leave)
    leave6.change_font(18)
    leave6.active = False
    buttons.append(leave6)

    return buttons

def load_world_buttons():
    buttons : list[button.TextureButton] = []

    remove_tile = button.TextureButton((0, 0), (64, 64), select_owner_no)
    remove_tile.load_texture(DEFAULT_UI_PATH + "world/RemoveTile.png")
    remove_tile.set_highlight(True)
    buttons.append(remove_tile)

    owner0 = button.TextureButton((0, 0), (64, 64), select_owner0)
    owner0.load_texture(DEFAULT_UI_PATH + "world/Owner0.png")
    buttons.append(owner0)

    owner1 = button.TextureButton((0, 0), (64, 64), select_owner1)
    owner1.load_texture(DEFAULT_UI_PATH + "world/Owner1.png")
    buttons.append(owner1)

    owner2 = button.TextureButton((0, 0), (64, 64), select_owner2)
    owner2.load_texture(DEFAULT_UI_PATH + "world/Owner2.png")
    buttons.append(owner2)

    owner3 = button.TextureButton((0, 0), (64, 64), select_owner3)
    owner3.load_texture(DEFAULT_UI_PATH + "world/Owner3.png")
    buttons.append(owner3)

    owner4 = button.TextureButton((0, 0), (64, 64), select_owner4)
    owner4.load_texture(DEFAULT_UI_PATH + "world/Owner4.png")
    buttons.append(owner4)

    owner5 = button.TextureButton((0, 0), (64, 64), select_owner5)
    owner5.load_texture(DEFAULT_UI_PATH + "world/Owner5.png")
    buttons.append(owner5)

    owner6 = button.TextureButton((0, 0), (64, 64), select_owner6)
    owner6.load_texture(DEFAULT_UI_PATH + "world/Owner6.png")
    buttons.append(owner6)

    remove_doodad = button.TextureButton((0, 0), (64, 64), select_doodad_no)
    remove_doodad.load_texture(DEFAULT_UI_PATH + "world/RemoveDoodad.png")
    remove_doodad.set_doodad_state()
    remove_doodad.set_highlight(True)
    buttons.append(remove_doodad)

    unit1 = button.TextureButton((0, 0), (64, 64), select_doodad_unit1)
    unit1.load_texture(DEFAULT_UI_PATH + "world/Unit_1.png")
    unit1.set_doodad_state()
    buttons.append(unit1)

    unit2 = button.TextureButton((0, 0), (64, 64), select_doodad_unit2)
    unit2.load_texture(DEFAULT_UI_PATH + "world/Unit_2.png")
    unit2.set_doodad_state()
    buttons.append(unit2)

    unit3 = button.TextureButton((0, 0), (64, 64), select_doodad_unit3)
    unit3.load_texture(DEFAULT_UI_PATH + "world/Unit_3.png")
    unit3.set_doodad_state()
    buttons.append(unit3)

    unit4 = button.TextureButton((0, 0), (64, 64), select_doodad_unit4)
    unit4.load_texture(DEFAULT_UI_PATH + "world/Unit_4.png")
    unit4.set_doodad_state()
    buttons.append(unit4)

    tower1 = button.TextureButton((0, 0), (64, 64), select_doodad_tower1)
    tower1.load_texture(DEFAULT_UI_PATH + "world/Tower_1.png")
    tower1.set_doodad_state()
    buttons.append(tower1)

    tower2 = button.TextureButton((0, 0), (64, 64), select_doodad_tower2)
    tower2.load_texture(DEFAULT_UI_PATH + "world/Tower_2.png")
    tower2.set_doodad_state()
    buttons.append(tower2)

    # main_base = button.TextureButton((0, 0), (64, 64), select_doodad_base)
    # main_base.load_texture(DEFAULT_UI_PATH + "world/Base.png")
    # main_base.set_doodad_state()
    # buttons.append(main_base)

    farm = button.TextureButton((0, 0), (64, 64), select_doodad_farm)
    farm.load_texture(DEFAULT_UI_PATH + "world/Farm.png")
    farm.set_doodad_state()
    buttons.append(farm)

    tree1 = button.TextureButton((0, 0), (64, 64), select_doodad_tree)
    tree1.load_texture(DEFAULT_UI_PATH + "world/Tree_1.png")
    tree1.set_doodad_state()
    buttons.append(tree1)

    grave1 = button.TextureButton((0, 0), (64, 64), select_doodad_grave)
    grave1.load_texture(DEFAULT_UI_PATH + "world/Grave_1.png")
    grave1.set_doodad_state()
    buttons.append(grave1)

    return buttons

