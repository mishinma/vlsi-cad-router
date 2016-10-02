from cell import *

PRED_DICT = {N: (0, 1, 0),
             S: (0, -1, 0),
             E: (1, 0, 0),
             W: (-1, 0, 0),
             U: (0, 0, 1),
             D: (0, 0, -1)}

OPDIR_DICT = {N: S,
              S: N,
              W: E,
              E: W,
              U: D,
              D: U}


UNITCOST = 1

elementwise_sum = lambda a, b: a+b
elementwise_prod = lambda a, b: a*b


class GridCell(Cell):
    """
    Each cell in a routing grid should contain:
        - predecessor (def None)
        - cost (def UNITCOST)
        - reached (True/False, def False)
    """

    def __init__(self, pred=None, cost=UNITCOST):
        super().__init__(pred)
        self.cost = cost
        self.reached = False


class RoutingGrid():
    """
    2D array of cells per layer
    x_
    """

    def __init__(self, x_size, y_size, layer_size, costs=None, bend_penalty=None, via_penalty=None):
        """
        Initialises the grid with (X, Y) 2D list (row based) with unit cost cells
        or cells with other costs if provided
        :param costs: list of list of costs, row based [[costs for 1st row where y=0] ... ]
                      if not provided then init with unitcost
        :param size: (X grid size, Y grid size)
        """

        self.l_size = layer_size
        self.x_size = x_size
        self.y_size = y_size
        self.size = (self.x_size, self.y_size, self.l_size)

        self.cells = [[[GridCell(cost=costs[_l][_y][_x] if costs is not None else UNITCOST)
                        for _x in range(self.x_size)]
                            for _y in range(self.y_size)]
                                for _l in range(self.l_size)]

        self.bend_penalty = bend_penalty if bend_penalty is not None else 0
        self.via_penalty = via_penalty if via_penalty is not None else 0

    def at(self, x, y, l):
        """
        :return: cell from routing grid an coordinates (x, y, l)
                [[[row 0], [row1] ... [row y-1]], ... [layer2]]
        """
        return self.cells[l][y][x]

    def within(self, x, y, l):
        """
        :return: True is cell coordinates is within the grid
        """
        return x in range(self.x_size) and y in range(self.y_size) and l in range(self.l_size)

    def cost_at(self, x, y, l):
        """
        :return: cost of the cell from (x,y,l)
        """
        return self.at(x, y, l).cost

    def is_obstacle(self, x, y, l):
        """
        If the cell is an obstacle its cost is -1
        :param x:
        :param y:
        :return: True if is obstacle, False if is free to route        """
        return self.at(x, y, l).cost == -1

    def is_reached(self, x, y, l):
        """
        :return true if cell is reached indeed
        """
        return self.at(x, y, l).reached

    def mark_reached(self, x, y, l):
        self.at(x, y, l).reached = True

    def mark_predecessor(self, x, y, l, pred):
        self.at(x,y,l).pred = pred

    def backtrace_path(self, source_cell, target_cell):
        """
        Follow pred(C) from the target cell to the source cell
        :param grid:
        :param source_cell: (s_x, s_y, s_l)
        :param target_cell: (t_x, t_y, t_l)
        :return: list of every cell on the path, in order, from the source to the target [(x,y,l), (x,y,l) ... ]
        """
        trace_cell = target_cell

        path = [trace_cell]

        while trace_cell != source_cell:
            trace_cell = tuple(map(elementwise_sum, trace_cell,
                                                PRED_DICT[self.at(*trace_cell).pred]))
            path.append(trace_cell)
        self.clean_up(path)
        path.reverse()
        return path

    def clean_up(self, path):
        """
        Clean up the grid for the next net, leaving the path as obstacle
        :param path:
        :return:
        """
        for path_cell in path:
            self.at(*path_cell).cost = -1
        # mark every cell as unreached
        for coords in self.gen_all_coordinates():
            self.at(*coords).reached = False

    def gen_all_coordinates(self):
        """
        :return: generator objects with all coordinates in the grid
        """
        for _l in range(self.l_size):
            for _y in range(self.y_size):
                for _x in range(self.x_size):
                    yield _x, _y, _l

    def gen_neighbors(self, home_cell):
        """
        Generator of unreached neighbors of home cell at (x,y,l)
        :param x:
        :param y:
        :return: Neighbor_cell (x, y, layer, cost, pred)
        """
        for pred_label, pred_shift in PRED_DICT.items():
            neighbor_cell = tuple(map(elementwise_sum, home_cell, pred_shift))
            if self.within(*neighbor_cell):
                if not self.is_reached(*neighbor_cell) and not self.is_obstacle(*neighbor_cell):
                    yield neighbor_cell, self.cost_at(*neighbor_cell), OPDIR_DICT[pred_label]


    @classmethod
    def read_grid_from_file(cls, filename):
        with open(filename, 'rt') as f:
            # First_line: 4 integers: X grid size (columns), Y grid size (rows), Bend penalty, Via penalty
            x_size, y_size, bend_penalty, via_penalty = [int(_) for _ in f.readline().split()]
            # Tne next lines Y specify the cost associated with each grid in LAYER 1
            # Tne next lines X specify the cost associated with each grid in LAYER 2

            costs = [[int(_) for _ in line.split()] for line in f.readlines()]
            costs_layer1 = costs[:y_size]
            costs_layer2 = costs[y_size:]

            return cls(x_size, y_size, layer_size=2, costs=[costs_layer1, costs_layer2],
                       bend_penalty=bend_penalty, via_penalty=via_penalty)






