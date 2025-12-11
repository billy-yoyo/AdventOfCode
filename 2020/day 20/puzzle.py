

tiles = []
border_offets = [
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0)
]

class Tile:
    def __init__(self, id, lines):
        self.id = id
        self.pos = (0, 0)
        self.borders = [
            lines[0],
            "".join(line[-1] for line in lines),
            lines[-1],
            "".join(line[0] for line in lines)
        ]

    def flip(self):
        # only flip horizontal borders
        for i in range(0, len(self.borders), 2):
            self.borders[i] = self.borders[i][::-1]

    def rotate(self, n):
        for _ in range(n % 4):
            self.borders = [self.borders[-1]] + self.borders[:-1]

    def flip_and_rotate(self, flip=False, rotation=0):
        if flip:
            self.flip()
        self.rotate(rotation)

    def placed(self, grid):
        return self.pos in grid and grid[self.pos].id == self.id
    
    def iterate_placements(self, grid, tile):
        for i, border in enumerate(self.borders):
            if self.placement_possible(grid, i):
                for j, tile_border in enumerate(tile.borders):
                    if border == tile_border:
                        yield (i, j)
                    if border == tile_border[::-1]:
                        yield (i, j + 4)

    def place(self, grid, tile, i, j):
        rotation = (i - j) - 2
        flip = j >= 4
        offset = border_offets[i]

        tile.flip_and_rotate(rotation=rotation, flip=flip)
        tile.pos = (offset[0] + self.pos[0], offset[1] + self.pos[1])
        grid[tile.pos] = tile

    def placement_possible(self, grid, i):
        offset = border_offets[i]
        return (offset[0] + self.pos[0], offset[1] + self.pos[1]) not in grid

    def find_neighbours(self, grid, tiles):
        for tile in tiles:
            if tile.id != self.id and not tile.placed(grid):
                for placement in self.iterate_placements(grid, tile):
                    yield tile, placement

    def is_corner(self, tiles):
        possible_neighbours = sum(1 for tile in self.find_neighbours({}, tiles))
        return possible_neighbours == 2

    def possible_neighbours(self, tiles):
        return sum(1 for tile in tiles if tile.id != self.id and any(b1 == b2 or b1 == b2[::-1] for b1 in self.borders for b2 in tile.borders))
            
    def __eq__(self, tile):
        return self.id == tile.id

    def __str__(self):
        return str(self.id)

def read_tile(data):
    data = data.strip()
    if not data:
        return

    lines = data.split("\n")
    tile_id = int(lines[0][5:-1])
    lines = [line.strip() for line in lines[1:]]
    tiles.append(Tile(tile_id, lines))

with open("data") as f:
    for data in f.read().split("\n\n"):
        read_tile(data)

def iterate_all_placements(grid, tile, placed):
    for placed_tile in placed:
        if placed_tile.id == tile.id:
            continue
            
        for placement in placed_tile.iterate_placements(grid, tile):
            yield placed_tile, placement

def get_boundaries(grid):
    minx, maxx = min(grid, key=lambda k: k[0])[0], max(grid, key=lambda k: k[0])[0]
    miny, maxy = min(grid, key=lambda k: k[1])[1], max(grid, key=lambda k: k[1])[1]

    return minx, maxx, miny, maxy

def get_corners(grid):
    minx, maxx, miny, maxy = get_boundaries(grid)
    return [(minx, miny), (minx, maxy), (maxx, miny), (maxx, maxy)]

def corners_placed(grid):
    return all(corner in grid for corner in get_corners(grid))

def place_remaining_tiles(grid, placed, remaining):
    print(len(remaining))
    if not remaining:
        yield grid
        #if corners_placed(grid):
        #    yield grid
        #return

    for tile in remaining:
        for placed_tile, placement in iterate_all_placements(grid, tile, placed):
            placed.append(tile)
            remaining.remove(tile)
            placed_tile.place(grid, tile, *placement)
            yield from place_remaining_tiles(grid, placed, remaining)

            # unplace tile
            del grid[tile.pos]
            remaining.append(tile)
            placed.remove(tile)


def place_all_tiles():
    start_tile = tiles[0]
    start_tile.pos = (0, 0)
    placed = [start_tile]
    remaining = tiles[1:]
    grid = {(0, 0): start_tile}

    while remaining:
        new_remaining = []
        for tile in remaining:
            for placed_tile, (i, j) in iterate_all_placements(grid, tile, placed):
                remaining.append(tile)
                placed_tile.place(grid, tile, i, j)
                break
            else:
                new_remaining.append(tile)
        remaining = new_remaining
    
    return grid
        
def print_grid(grid):
    minx, maxx, miny, maxy = get_boundaries(grid)
    print("\n".join("".join("x" if (x, y) in grid else "." for x in range(minx, maxx + 1)) for y in range(miny, maxy + 1)))
"""
for tile in tiles:
    n = tile.possible_neighbours(tiles)
    if n != 4:
        print(f"tile {tile} has {n} possible neighbours")
    else:
        print(f"tile {tile} is correct")"""

grid = place_all_tiles()
print_grid(grid)
