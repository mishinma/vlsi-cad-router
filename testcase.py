import unittest
from cell import N, S, E, W, U, D
from routing_grid import GridCell, RoutingGrid, UNITCOST
from wavefront import WavefrontCell, Wavefront
from netlist import Net, read_netlist_from_file



class TestConstructionCell(unittest.TestCase):

    def test_cell(self):
        c = GridCell()
        self.assertIsNone(c.pred)
        self.assertEqual(c.cost, UNITCOST)
        self.assertFalse(c.reached)

    def test_cell_nonunit_cost(self):
        c = GridCell(cost=5, pred=U)
        self.assertFalse(c.reached)
        self.assertEqual(c.cost, 5)
        self.assertEqual(c.pred, U)


class TestConstructionGrid(unittest.TestCase):

    def setUp(self):
        self.costs = [[[1, 1, 1], [2, 2, 2], [3, 3, 3]]]

    def test_grid(self):
        g = RoutingGrid(6,6,1)
        self.assertEqual(g.cost_at(2, 1, 0), UNITCOST)

    def test_grid_with_nonunit_cost(self):
        f = RoutingGrid(3, 3, 1, costs=self.costs)
        y=0 # 1st row from the bottom
        for x in range(3):
            self.assertEqual(f.cost_at(x,y,0), UNITCOST)
        y=1 # 2nd row
        for x in range(3):
            self.assertEqual(f.cost_at(x,y,0), 2)
        y=2 # 2nd row
        for x in range(3):
            self.assertEqual(f.cost_at(x,y,0), 3)

    def test_within(self):
        g = RoutingGrid(4,4,2)
        self.assertTrue(g.within(3,3,1))
        self.assertFalse(g.within(4,0,0))
        self.assertFalse(g.within(-1,0,1))

class TestWaveFrontConstruction(unittest.TestCase):

    def setUp(self):
        self.grid = RoutingGrid(4,4,1)
        self.c1 = WavefrontCell(1,1,0,10,U)
        self.c2 = WavefrontCell(1,2,0,10,D)
        self.c3 = WavefrontCell(3,1,0,5,U)
        self.c4 = WavefrontCell(2,1,0,1,U)
        self.c5 = WavefrontCell(1,3,0,15,W)
        self.tc = WavefrontCell(3,1,0)
        self.source_cell = WavefrontCell(1,4,0,10)

    def test_equal_to(self):
        self.assertTrue(self.c3.equal_coord(self.tc))

    def test_init_source_cell(self):
        self.assertIsNone(self.source_cell.pred)

    def test_wavefrontcell_eq_pos(self):
        self.assertTrue(self.c1 == self.c2)

    def test_wavefrontcell_ne_neg(self):
        self.assertTrue(self.c1 != self.c3)

    def test_wavefrontcell_eq_pos(self):
        self.assertFalse(self.c1 == self.c3)

    def test_wavefrontcell_ne_neg(self):
        self.assertFalse(self.c1 != self.c2)

    def test_wavefrontcell_le_pos1(self):
        self.assertTrue(self.c1 <= self.c2)

    def test_wavefrontcell_le_pos2(self):
        self.assertTrue(self.c4 <= self.c2)

    def test_wavefrontcell_le_neg(self):
        self.assertFalse(self.c3 <= self.c4)

    def test_wavefront(self):
        wf = Wavefront(self.c1, self.c3, self.c4, grid=RoutingGrid(6,6,1))

    def test_heap_functionality(self):
        wf = Wavefront(self.c5, self.c1, grid=self.grid)
        wf.insert(self.grid, self.c2, self.c3, self.c4)
        self.assertTrue(self.grid.is_reached(1,1,0))
        self.assertTrue(self.grid.is_reached(1,3,0))
        self.assertEqual(wf.ditto().pathcost, self.c4.pathcost)
        self.assertEqual(wf.ditto().pathcost, self.c3.pathcost)
        self.assertEqual(wf.ditto().pathcost, self.c1.pathcost)
        self.assertEqual(wf.ditto().pathcost, self.c2.pathcost)
        self.assertEqual(wf.ditto().pathcost, self.c5.pathcost)
        with self.assertRaises(IndexError):
            wf.ditto()


class TestReadingInputFiles(unittest.TestCase):

    def test_read_grid_input_file(self):
        g = RoutingGrid.read_grid_from_file('toy1.grid')
        self.assertEqual(g.size, (6, 5, 2))
        self.assertEqual(g.cost_at(3,0,0), 5)
        self.assertEqual(g.cost_at(4,1,0), 4)
        self.assertEqual(g.cost_at(4,3,0), -1)
        self.assertTrue(g.is_obstacle(4,3,0))


class TestNetlistConstruction(unittest.TestCase):

    def test_netlist(self):
        n1 = Net(1, 1, 0, 4, 1, 2, 0)
        n2 = Net(2, 1, 2, 3, 2, 3, 3)
        n3 = Net(3, 2, 2, 1, 2, 5, 0)
        netlist = [n1, n2, n3]

    def test_netlist_read_from_input(self):
        netlist = read_netlist_from_file('toy1.nl')


class TestOneLayerUnitCostRouter(unittest.TestCase):

    def setUp(self):
        self.g = RoutingGrid.read_grid_from_file('bench1.grid')
        self.nl = read_netlist_from_file('bench1.nl')

    def test_backtrace_path(self):
        g = RoutingGrid(3,3,1)
        g.at(1,2,0).pred = W
        g.at(2,2,0).pred = W
        g.at(2,1,0).pred = N
        g.at(1,1,0).pred = E
        g.at(1,0,0).pred = N
        g.at(2,0,0).pred = W
        p = g.backtrace_path((0,2,0),(2,0,0))
        self.assertEqual(p, [(2,0,0), (1,0,0), (1,1,0), (2,1,0), (2,2,0), (1,2,0), (0,2,0)])
        self.assertEqual([g.cost_at(0,2,0), g.cost_at(1,2,0), g.cost_at(2,2,0), g.cost_at(2,1,0), g.cost_at(1,1,0),
                          g.cost_at(1,0,0), g.cost_at(2,0,0)], [-1]*7 )
        self.assertFalse(g.is_reached(1,1,0))

    def test_find_neighbors(self):
        g = RoutingGrid(3,3,2)
        g.mark_reached(0,0,0)
        n = g.gen_neighbors((0,0,0))
        coo1, cost1, pred1 = next(n)
        self.assertEqual(coo1, (0,1,0))
        self.assertEqual(cost1, UNITCOST)
        self.assertEqual(pred1, S)
        coo2, cost2, pred2 = next(n)
        self.assertEqual(coo2, (1,0,0))
        self.assertEqual(cost2, UNITCOST)
        self.assertEqual(pred2, W)
        coo3, cost3, pred3 = next(n)
        self.assertEqual(coo3, (0,0,1))
        self.assertEqual(cost3, UNITCOST)
        self.assertEqual(pred3, D)
        with self.assertRaises(StopIteration):
            next(n)

    def test_expand(self):
        g = RoutingGrid(3,3,1)
        s_cell = WavefrontCell(0,0,0,g.cost_at(0,0,0))
        wf = Wavefront(s_cell, grid=g)
        wf.expand(g)
        self.assertEqual(wf.length(),2)
        c = wf.ditto()
        self.assertEqual(c.pathcost, 2)
        self.assertTrue(c.pred == S or c.pred == W)
        self.assertTrue(g.is_reached(0,1,0))
        self.assertTrue(g.is_reached(1,0,0))
        self.assertFalse(g.is_reached(1,1,0))
        self.assertEqual(g.at(0,1,0).pred, S)
        self.assertEqual(g.at(1,0,0).pred, W)
        wf.insert(g,c)
        wf.expand(g)
        self.assertEqual(wf.length(), 3)

if __name__ == '__main__':
    unittest.main()
