'''Generate grids using invasion percolation.'''

from .params import GridParams, load_params
from pathlib import Path
import polars as pl
import random


class Grid:
    '''Represent a lazy grid.'''

    def __init__(self, params):
        '''Record shared state.'''
        self._width = params.width
        self._height = params.height
        self._depth = params.depth
        self._grid = []
        for x in range(self._width):
            col = []
            for y in range(self._height):
                col.append(random.randint(1, self._depth))
            self._grid.append(col)
        self._candidates = {}

    def __getitem__(self, key):
        '''Get value at location.'''
        x, y = key
        return self._grid[x][y]

    def __setitem__(self, key, value):
        '''Set value at location.'''
        x, y = key
        self._grid[x][y] = value

    def __str__(self):
        '''Convert to printable string.'''
        rows = []
        for y in range(self.height() - 1, -1, -1):
            rows.append(''.join('x' if self[x, y] == 0 else '.' for x in range(self.width())))
        return '\n'.join(rows)

    def depth(self):
        '''Get depth of grid.'''
        return self._depth

    def height(self):
        '''Get height of grid.'''
        return self._height

    def width(self):
        '''Get width of grid.'''
        return self._width

    def fill(self):
        '''Fill grid one cell at a time.'''
        x, y = self.width() // 2, self.height() // 2
        self[x, y] = 0
        self.add_candidates(x, y)
        while True:
            x, y = self.choose_cell()
            self[x, y] = 0
            if self.on_border(x, y):
                break

    def add_candidates(self, x, y):
        '''Add candidates around (x, y).'''
        for ix in (x - 1, x + 1):
            self.add_one_candidate(ix, y)
        for iy in (y - 1, y + 1):
            self.add_one_candidate(x, iy)

    def add_one_candidate(self, x, y):
        '''Add (x, y) if suitable.'''
        if (x < 0) or (x >= self.width()) or (y < 0) or (y >= self.height()):
            return
        if self[x, y] == 0:
            return

        value = self[x, y]
        if value not in self._candidates:
            self._candidates[value] = set()
        self._candidates[value].add((x, y))

    def adjacent(self, x, y):
        '''Is (x, y) adjacent to a filled cell?'''
        x_1, y_1 = x + 1, y + 1
        if (x > 0) and (self[x - 1, y] == 0):
            return True
        if (x_1 < self.width()) and (self[x_1, y] == 0):
            return True
        if (y > 0) and (self[x, y - 1] == 0):
            return True
        if (y_1 < self.height()) and (self[x, y_1] == 0):
            return True
        return False

    def choose_cell(self):
        '''Choose the next cell to fill.'''
        min_key = min(self._candidates.keys())
        available = list(sorted(self._candidates[min_key]))
        i = random.randrange(len(available))
        choice = available[i]
        del available[i]
        if not available:
            del self._candidates[min_key]
        else:
            self._candidates[min_key] = set(available)
        self.add_candidates(*choice)
        return choice

    def on_border(self, x, y):
        '''Is this cell on the border of the grid?'''
        if (x == 0) or (x == self.width() - 1):
            return True
        if (y == 0) or (y == self.height() - 1):
            return True
        return False


def grid(options):
    '''Main driver.'''
    options.params = load_params(GridParams, options.params)
    options.sites = pl.read_csv(options.sites)
    random.seed(options.params.seed)
    for row in options.sites.iter_rows(named=True):
        grid = Grid(options.params)
        grid.fill()
        _save(options.outdir, row['site_id'], grid)


def _save(outdir, site_id, grid):
    '''Save grid as CSV.'''
    rows = []
    for y in range(grid.height() - 1, -1, -1):
        rows.append(','.join('1' if grid[x, y] == 0 else '0' for x in range(grid.width())))
    with open(Path(outdir, f'{site_id}.csv'), 'w') as writer:
        print('\n'.join(rows), file=writer)
