# Hex-Wars: Software Architecture Documentation

## 1. Introduction

### 1.1 Project Overview
Hex-Wars is a 2D top-down turn-based strategy game inspired by classic territory control games Antiyoy and Slay. Players compete to control hexagonal territories on a map by strategically placing units and structures while managing income and money reserve. Controlling more territory will yield more income, while having more army will deplete it. The army will desert if money reaches negative. The territory can be split into separate states that act independently during the same turn, having independent units, structures, income and money.

### 1.2 Core Functionalities
The game will implement the following key features:
- **Turn-based gameplay**: Players take alternating turns to move units, construct buildings, and expand territory
- **Hexagonal grid system**: Map composed of hex tiles with different terrain types
- **Economic management**: Structures generate income, as well as controlling hexes; units and buildings consume resources
- **Unit management**: Create, move, and command military units across hexes
- **Structure building**: Construct various buildings (towers and farms) that provide strategic advantages
- **Map Editor**: Standalone tool for creating custom maps with territory painting and starting position setup, as well as player order, starting balance and army
- **Save/Load system**: Persistent game state and custom map storage using pickle serialization
- **Local multiplayer**: Hot-seat gameplay for 2-8 players on the same device

- ### 1.3 Target Users
- Strategy game enthusiasts who enjoy tactical, turn-based gameplay
- Players who appreciate simple mechanics with strategic depth
- Map creators interested in designing custom scenarios
- Users who may prefer a shorter, more condensed turn-based gameplay

### 1.4 Technology Stack & Constraints
- **Primary Language**: Python 3.10+
- **Graphics/Game Engine**: Pygame 2.x for rendering, input handling, and game loop
- **Serialization**: Pickle for save file management
- **Deployment**: Standalone desktop application (Windows/Linux/macOS)
- **Development Constraints**: Local multiplayer only (no networking), no bots/AI, game may lag when handling large maps

- ## 2. System Overview

### 2.1 High-Level Architecture
Hex-Wars follows a **Model-View-Controller (MVC)** architectural pattern adapted for game development:

```
┌─────────────────────────────────────────┐
│         Game Application                │
│  ┌─────────────────────────────────┐    │
│  │   Main Game Loop (Pygame)       │    │
│  └─────────────────────────────────┘    │
│                  │                      │
│      ┌───────────┼────────────┐         │
│      │           │            │         │
│   ┌──▼───┐   ┌───▼────┐   ┌───▼────┐    │
│   │ View │   │ Model  │   │Control │    │
│   │Layer │◄──┤ Layer  │──►│ Layer  │    │
│   └──────┘   └────────┘   └────────┘    │
│                  │                      │
│         ┌────────┴───────┐              │
│    ┌────▼─────┐   ┌──────▼─────┐        │
│    │ Save/Load│   │ Map Editor │        │
│    │  System  │   │   Module   │        │
│    └──────────┘   └────────────┘        │
└─────────────────────────────────────────┘
```

### 2.2 Core Components
1. **Model Layer**: Game state, entities (units, structures, hexes), game logic
2. **View Layer**: Rendering system, UI elements
3. **Control Layer**: Input handling, game state management, turn logic
4. **Persistence System**: Save/load maps and current games
5. **Map Editor**: Separate module for user map creation

### 2.3 Design Patterns
- **Compound pattern**: Units and structures share common behaviors through composition
- **State pattern**: Game states (menu, gameplay, map editor)

### 2.4 Data Flow
1. User input captured by Pygame event system
2. Control layer processes input and updates model
3. Model validates actions and updates game state
4. View layer queries model and renders to screen
5. Save system serializes model state to disk when requested

## 3. Detailed Component Design

### 3.1 Model Layer

#### 3.1.1 Core Classes

**`Hex`**
- A tile from the map
- Attributes: `owner`, `doodad (a.k.a. unit, structure or tree)`, `position`, `income`, `is_central_hex`
- Methods: `get_position()`, `get_doodad()`

**`HexMap`**
- Stores the game map as a 2D array of Hex objects
- Attributes: `dimensions`, `hex_map[]`
- Methods: `get_hexmap()`, `get_hex_all_neighbors(hex)`, `get_hex_from_pos(x, y)`, `fill_map(default_owner = 0)`
- Implements axial coordinate system for hexagonal grids

**`State`**
- Stores the hexes forming the state, as well as income and money of the state
- Attributes: `income`, `money`, `is_bankrupt`, `hexes[]`
- Methods: `update_income()`, `hex_march() (for getting all hexes of the state)`, `split_state()`, `merge_states(state_list)`

**`Player`**
- Stores some information about the player, as well as a list of State objects
- Attributes: `owner`, `color`, `states[]`
- Methods: `add_state(state)`, `get_states()`, `handle_turn()`

**`Doodad`**
- Base class for all things that sit on a hex
- Attributes: `income`
- Methods: `get_type`, `get_name`
- Subclasses: `Controllable`, `Tree`

**`Controllable`**
- Base class for all units and structures, inherited from `Doodad`
- Attributes: `owner`
- Subclasses: `Unit`, `Structure`

**`Unit`**
- Base class for all military units, inherited from `Controllable`
- Attributes: `sight_range`, `move_range`, `defence`, `attack`, `type`
- Subclasses: `UnitTier1`, `UnitTier2`, `UnitTier3`, `UnitTier4`

**`Structure`**
- Base class for buildings
- Attributes: `sight_range`, `defence`, `type`
- Subclasses: `TowerTier1`, `TowerTier2`, `TownCenter`, `Farm`

**`GameRenderer`**
- Class for handling the rendering of the map, alongside getting tile at mouse coordinates
- It splits the map into chunks of images, rendering only what is being seen (lazy rendering). This allows for (theoretically) infinite maps in size
- Attributes: `zoom_settings`, `color_scheme`, `chunks[][]`, `visible_chunks[][]`, `background`
- Methods: `reload_renderer(hexmap object)`, `set_zoom(new_zoom)`, `init_chunks()`, `draw_tile(hex object, chunk surface)`, `get_visible_chunks()`, `update_chunk(hex object)`, `draw_chunks()`

**`Editor`**
- Handles the map editor
- Attributes: `config (map configuration for saving)`
- Methods: `load_game(game_name)`, `save_game(game_name)`

#### 3.1.2 Game Logic
- **Economy System**: Each turn, calculate `total_income = Σ(hex_income) + Σ(structure_bonuses) - Σ(unit_upkeep) - Σ(structure_upkeep)`
- **Combat Resolution**: Simple attack vs defense calculation
- **Territory Control**: Hexes captured when no enemy units remain and owner places unit/structure

### 3.2 Map Editor Module

#### 3.2.1 Editor Core
**`MapEditor`**
- Standalone mode accessible from main menu
- Tools: `brush size`, `draw`, `fill`, `undo`, `redo`, `tile picker`, `center map`, `select owner`, `select doodad`, `select starting money`, `select map dimensions`

## 4. Deployment and Testing

### 4.1 System Requirements
- **OS**: Windows 10+, Linux (Ubuntu 20.04+), macOS 10.15+
- **Python**: Version 3.10 or higher
- **Dependencies**: Pygame 2.x (installable via pip)
- **Storage**: ~5MB for application, additional space for saves/maps

### 4.2 Deployment Strategy
- **Distribution**: Packaged as executable
- **Package contents**: Game executable, default maps folder, README
- **Installation**: Extract and run (portable application, no installation required)

### 4.3 Configuration
- Save files stored in game folder: `maps/game` or `saves`
- Custom maps in: `maps/custom`

### 4.4 Testing Strategy
- **Manual testing approach**: Primary testing method for this project
- **Test areas**:
  - Core gameplay loop (turn transitions, unit movement, combat)
  - Economic system (income calculation, upkeep deduction)
  - Save/load functionality (state persistence across sessions)
  - Map editor (map creation, validation, export/import)
  - Edge cases (invalid moves, bankruptcy, victory conditions)
- **Playtesting**: Multiple complete games to ensure balance and identify bugs
- **Unit tests**: Optional Python unittest framework for critical logic (pathfinding, economy calculations)

## 5. Conclusion

### 5.1 Project Summary
Hex-Wars aims to deliver a polished turn-based strategy experience using proven gameplay mechanics from Antiyoy and Slay, adapted with modern Python development practices. The MVC architecture provides clear separation of concerns, making the codebase maintainable and extensible.

### 5.2 Complexity Assessment
**Moderate complexity**. The hexagonal grid mathematics and pathfinding algorithms present the primary technical challenges. The economic system, while conceptually simple, requires careful balancing.
Pygame provides adequate tooling for rendering and input, reducing graphics programming complexity, though some optimisations were required to make rendering as smooth as possible, while allowing for big maps

### 5.3 Estimated Development Time
- A bit challenging to estimate, especially at the current state of the project, but if there needed to be a hard guess:
- **Total**: 80-110 hours over 7-9 weeks
- Breakdown:
  - Core game engine (hex grid, rendering): 30-35 hours
  - Game logic (units, combat, economy): 25-30 hours
  - UI and menu systems: 10-15 hours
  - Map editor: 15-20 hours
  - Save/load system: 4-5 hours
  - Testing, balancing, polish: 3-4 hours

### 5.4 Learning Requirements
- **Hexagonal grid mathematics**: Axial coordinate systems, cube coordinates, hex-to-pixel conversion
- **Pygame fundamentals**: Event handling, surface manipulation, sprite management
- **Pathfinding algorithms**: BFS for pathfinding, and state population
- **Python serialization**: Understanding pickle's capabilities and limitations
- **Game design principles**: Turn-based strategy balance, economic systems, win conditions

### 5.5 Afterthoughts
I think we picked a project too big for our current level and time. Even though it was fun to work on this project, it feels a bit too much, and the hours estimated prove this. 
We wanted for some time to build this exact project, and were very glad for the opportunity to kill two birds with one stone. With more work, this could be a solid game that's moderately complex, but that's outside of the current scope.
For this project, only the minimum gameplay mechanics will be present.
