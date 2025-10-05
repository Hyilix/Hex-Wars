Python project (name in progress)
=================================

# Various game ideas

Game name (up for serious debate):
  - Hexia
  - Hexo-war
  - Hex wars

Legend:
  - ¿sentence? -> means just a thought. Most of the times, it refers to potential game features 
  - # sentence -> means a new idea/concept not present in the original antiyoy. Usually it refers to changed gameplay features. 

Premise:
  - A turn-based strategy game on a hexagonal grid where players (¿and/or bots?) fight for control of the map. 
  - The goal is to be the last player surviving on the map (¿or diplomacy?). 
  - Each tile can be controlled by any player using units. 
  - Each player starts with a predefined set of tiles, structures, units and money (¿and diplomacy?). 
  - Each unit/structure utilizes an amount of money to build. 
  - Each unit/structure consumea an amount of income to survive. Tiles and farm structures provide income, while units and tower structures deplete income. Also, doodads such as trees or rocks blocks the income of the tile.
  - Income means money per round. At the beginning of each round, the player will receive an equal amount of money with the income. 
  - Every section of your territory count as separate entities. For example, one continuous plane of controlled hexes and farm structures will generate the income, while units and tower structures deplete the income of one entity. However, if the entity is split by another player by cutting the territory physically, there will be two entities, each with their separate income. 
  - If the money reach below 0 at the start of any round (meaning negative income and no money), all the units of the respective entity will die, freeing the income consumed. 
  - Each tier of units can only attack units/towers of a lower tier, excluding the last tier, that can attack lower or equal tier. The higher the tier, the greater the cost/upkeep income. A unit/tower can defend all the controlled hexes adjacent to it (including the occupying hex). A unit can move freely in controlled territories up to a range, but can only attack one non-friendly hex adjacent to the territory, considering it can reach it. A For any hex, only the greatest tier is considered. 
  - All units can only perform one action each round, either attacking or moving. 
  - Only units are allowed to be moved. 
  - An entity of only one hex is not considered an entity, thus it will produce nothing, but it will remain controlled by the owner of the original entity. 
  - Each hex can only be occupied by one structure or one unit at any time. 
  - # Rivers in between two hexes may not be crosses by any unit. 
  - # Towers and units can defend adjacent hexes even separated by rivers. 
  - Fog of war restricts players from visualising the entire map at once. To gain vision, a player must use units or towers to detect nearby tiles. 

Expected Gameplay Features:
  - Local multiplayer with map selection and various settings which include: fog of war, starting money, ¿starting diplomacy?, ¿bot count?, ¿random map settings? etc. 
  - Core gameplay mechanics: building, attacking, unit moving, income, entity separation, player losing, fog of war. 
  - Zoom-in / Zoom-out the map. 
  - Menu, settings and lobby screens. 
  - In-game map editor. 

Potential Gameplay Features:
  - Random map generator. 
  - In-game diplomacy: Firendship, enemy, neutal states, land transfer, money transfer, income subsidies, ¿military acces?, ¿mercenaries?. 
  - Online multiplayer, with automatic map transfer
  vvv less likely from here vvv
  - # More complicated hex terrain: fertile land (2x income), forest (less visibility/movement), mountain (+1 defense, less movement, more visibility, invalid for structures) etc. (up for serious debate) 
(goes hand in hand with next point). 
  - # More structures: ballista (+1 attack for nearby units), monastery (+1 defense for nearby units) etc. (up for serious debate) (goes hand in hand with previous point).
  - Bots
  - # Naval warfare, naval supply, amphibious invasions, sea income. 
  - # Replace lost player with bot, hotjoin.

Basic Game Code Ideas:
  -  Unit inheritance structure:
     * Player (entities) 
     * Hex (income, doodad, ¿terrain?, river) 
     * Entity/state (income, money) 
     * Doodad (position, income) 
          * Tower (defence stat) 
          * Unit (defence/offence stats, movement) 
  - Hex map: a 2d array of Hex objects
