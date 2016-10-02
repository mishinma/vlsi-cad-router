from cell import *
from heapq import *


class WavefrontCell(Cell):
    """
    Each cell C in the wavefront stores:
        - coordinates in grid
        - layer of grid cell
        - pathcost of cell
        - predecessor of cell (tags N, S, E, W, UP, DOWN) in the dir from
            which cell C was reached

    """

    def __init__(self, x, y, layer, pathcost=None, pred=None):
        super().__init__(pred)
        self.x = x
        self.y = y
        self.layer = layer
        self.pathcost = pathcost


        @property
        def pathcost(self):
            return self._pathcost

        @pathcost.setter
        def pathcost(self, pathcost_value):
            self._pathcost = pathcost_value

    def coordinates(self):
        return self.x, self.y, self.layer

    def equal_coord(self, rhs):
        """
        :return true if equal coordinates and layer
        """
        return self.x == rhs.x and self.y == rhs.y and self.layer == rhs.layer


    def __le__(self, rhs):
        if not isinstance(rhs, WavefrontCell):
            return NotImplemented
        return self.pathcost <= rhs.pathcost

    def __ne__(self, rhs):
        if not isinstance(rhs, WavefrontCell):
            return NotImplemented
        return self.pathcost != rhs.pathcost

    def __eq__(self, rhs):
        if not isinstance(rhs, WavefrontCell):
            return NotImplemented
        return self.pathcost == rhs.pathcost

    def __lt__(self, rhs):
        if not isinstance(rhs, WavefrontCell):
            return NotImplemented
        return self.pathcost < rhs.pathcost

    def __gt__(self, rhs):
        if not isinstance(rhs, WavefrontCell):
            return NotImplemented
        return self.pathcost >= rhs.pathcost

    def __ge__(self, rhs):
        if not isinstance(rhs, WavefrontCell):
            return NotImplemented
        return self.pathcost >= rhs.pathcost


class Wavefront():
    """
    Store cells of wavefront in a HEAP, cost-based indexing
    """

    def __init__(self, *cells, grid=None):
        self.cells = []
        for cell in cells:
            self.insert(grid, cell) if grid is not None else TypeError

    def insert(self, grid, *cells):
        """
        When we insert cell in the wavefront we reach them
        :param cell: either cell or list of cells to be pushed to the heap
        :return:
        """
        for cell in cells:
            x,y,l = cell.coordinates()
            grid.mark_reached(x,y,l)
            grid.mark_predecessor(x,y,l,cell.pred)
            heappush(self.cells, cell)

    def ditto(self):
        return heappop(self.cells)

    def length(self):
        return len(self.cells)

    def expand(self, grid):
        """
        Pop cell form the wavefront, find its neighbors and add them to the wavefront
        :param grid:
        :param cell:
        """
        home_cell = self.ditto()
        for neighbor_coord, neighbor_cost, neighbor_pred in grid.gen_neighbors(home_cell.coordinates()):
            x, y, l = neighbor_coord
            # Pathcost computation
            # 1. If pred neighbor = U or D then there is via penalty
            # 2. If pred home = U or D and pred_home == pred_neighbor then there is no penalties
            # 3. Else bend_penalty

            neighbor_pathcost = neighbor_cost + home_cell.pathcost
            if neighbor_pred == U or neighbor_pred == D:
                neighbor_pathcost += grid.via_penalty
            elif home_cell.pred != neighbor_pred:
                neighbor_pathcost += grid.bend_penalty

            self.insert(grid, WavefrontCell(x,y,l,neighbor_pathcost,neighbor_pred))






