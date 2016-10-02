N = 0
S = 1
E = 2
W = 3
U = 4
D = 5


class Cell():
    """
    This is base class for GridCell and WavefrontCell
    Each cell  contain:
        - predecessor of cell (tags N, S, E, W, UP, DOWN) in the dir from
            which cell C was reached
    """

    def __init__(self, pred=None):
        self.pred = pred
