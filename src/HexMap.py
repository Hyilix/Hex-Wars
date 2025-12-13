import copy
from Hex import Hex
import random
from collections import deque

import ActionHandler

class HexMap:
    def __init__(self, x_tile_count : int, y_tile_count : int, default_owner : int = -1):
        self.dimensions = (x_tile_count, y_tile_count)
        self.hexmap = [[]]
        self.fill_map(default_owner)

    def change_map_size(self, x_count_new : int, y_count_new : int):
        self.dimensions = (x_count_new, y_count_new)

    def get_tile_at_position(self, tile_pos : tuple[int, int]):
        return self.hexmap[tile_pos[1]][tile_pos[0]]

    def fill_map(self, default_owner : int = -1):
        local_owner = default_owner
        for y in range(self.dimensions[1]):
            for x in range(self.dimensions[0]):
                # Get a random owner
                if default_owner == -2:
                    local_owner = random.randrange(0, 8)
                    # local_owner = 0
                    # if y % 8 == 0 and x % 8 == 0:
                    #     local_owner = 1

                self.hexmap[y].append(Hex(x, y, local_owner))
            self.hexmap.append([])

    def get_hex_from_pos(self, x_pos : int, y_pos : int):
        # Out of bounds check
        if x_pos < 0 or y_pos < 0 or x_pos >= self.dimensions[0] or y_pos >= self.dimensions[1]:
            return None
        return self.hexmap[y_pos][x_pos]

    def get_hexmap(self):
        return self.hexmap

    # Returns a neighbor of input index
    def get_hex_neighbor(self, tile : Hex, index : int):
        (tile_pos_x, tile_pos_y) = tile.get_position()
        index = index % 6

        # Check if tile exists
        if tile_pos_x == None or tile_pos_y == None:
            return None

        # Check all indeces
        if index == 0:
            tile_pos_y -= 1
        elif index == 1:
            tile_pos_x += 1
            tile_pos_y -= (tile_pos_x % 2)
        elif index == 2:
            tile_pos_x += 1
            tile_pos_y += 1
            tile_pos_y -= (tile_pos_x % 2)
        elif index == 3:
            tile_pos_y += 1
        elif index == 4:
            tile_pos_y += 1
            tile_pos_x -= 1
            tile_pos_y -= (tile_pos_x % 2)
        elif index == 5:
            tile_pos_x -= 1
            tile_pos_y -= (tile_pos_x % 2)

        return self.get_hex_from_pos(tile_pos_x, tile_pos_y)

    # Returns an array containing all 6 neighbors of a hex
    def get_hex_all_neighbors(self, tile : Hex):
        neighbors = []
        for index in range(6):
            neighbors.append(self.get_hex_neighbor(tile, index))
        return neighbors

    # Returns an array containing the neighboring tiles of a clump
    def get_neighbors_around_clump(self, clump : list[Hex], tiles):
        for current in clump:
            neighbors = self.get_hex_all_neighbors(current)

            for neighbor in neighbors:
                if neighbor and neighbor not in tiles and neighbor not in clump:
                    tiles.append(neighbor)

    def __bfs_up_to_level(self, start, max_level, only_identical = False):
        visited = [start]
        queue = deque([(start, 0)])

        while queue:
            tile, level = queue.popleft()
            if level < max_level or max_level == -1:
                for neighbour in self.get_hex_all_neighbors(tile):
                    if neighbour and neighbour not in visited:
                        if only_identical == False or start.is_hex_identical(neighbour):
                            visited.append(neighbour)
                            queue.append((neighbour, level + 1))

        return visited

    def get_movable_tiles(self, start, max_level):
        visited = [start]
        queue = deque([(start, 0)])

        while queue:
            tile, level = queue.popleft()
            if (level < max_level or max_level == -1) and tile.owner == start.owner:
                for neighbour in self.get_hex_all_neighbors(tile):
                    if neighbour and neighbour not in visited:
                        if not neighbour.doodad or neighbour.owner != start.owner:
                            visited.append(neighbour)
                            queue.append((neighbour, level + 1))

        return visited

    def get_identical_neighboring_hexes(self, tile : Hex):
        return self.__bfs_up_to_level(tile, -1, True)

    def get_neighbors_at_level(self, tile : Hex, levels : int):
        return self.__bfs_up_to_level(tile, levels - 1)

    # Move the unit from one hex to another
    def move_unit(self, start_hex : Hex, end_hex : Hex, action_list : ActionHandler.ActionList):
        if not start_hex or not end_hex:
            return

        print(f"start_hex -> {start_hex.get_position()}, end_hex -> {end_hex.get_position()}")

        # If there is no doodad, there is nothing to move
        if start_hex.doodad == None:
            return

        valid_tiles = self.get_movable_tiles(start_hex, start_hex.doodad.get_move_range())
        print(f"move range : {start_hex.doodad.get_move_range()}")
        # for tile in valid_tiles:
        #     print(f"valid tile -> {tile.get_position()}")

        if end_hex not in valid_tiles or not start_hex.doodad.get_can_action():
            return
        start_hex.doodad.set_can_action(False)

        print("Move the unit")

        action_list.add_action(ActionHandler.Action(ActionHandler.ActionType.TILE, copy.deepcopy(end_hex.doodad), copy.deepcopy(start_hex.doodad), 'doodad', end_hex))
        action_list.add_action(ActionHandler.Action(ActionHandler.ActionType.TILE, end_hex.owner, start_hex.owner, 'owner', end_hex))
        action_list.add_action(ActionHandler.Action(ActionHandler.ActionType.TILE, copy.deepcopy(start_hex.doodad), None, 'doodad', start_hex))

# Index of each neighbour
#            _____
#           /     \
#          /       \
#    ,----(    0    )----.
#   /      \       /      \
#  /        \_____/        \
#  \    5   /     \   1    /
#   \      /       \      /
#    )----(   self  )----(
#   /      \       /      \
#  /    4   \_____/   2    \
#  \        /     \        /
#   \      /       \      /
#    `----(    3    )----'
#          \       /
#           \_____/

