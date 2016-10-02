from routing_grid import RoutingGrid, GridCell
from wavefront import Wavefront, WavefrontCell
import netlist
import sys


def maze_algorithm(g, nl):

    # INITIALIZATION

    # Source cell and target cell from the net
    source_cell = net.s
    target_cell = net.t
    #print("Source cell {}".format(source_cell.coordinates()))

    #print("Target cell {}".format(target_cell.coordinates()))
    #print("{} : {}".format(source_cell.coordinates(),g.cost_at(*source_cell.coordinates())))
    #if g.cost_at(*source_cell.coordinates()) != -1:
    #    source_cell.pathcost = g.cost_at(*source_cell.coordinates())
    #else:
    #    return list()
    source_cell.pathcost = g.cost_at(*source_cell.coordinates())
    # Initialize wavefront and add source cell
    wf = Wavefront(source_cell, grid=g)

    while not g.is_reached(*target_cell.coordinates()):  # while we have not reached target cell
        if wf.length() == 0:
            print("No path to be found")
            return list() # no path to be found

        #EXPAND
        wf.expand(g)
        if g.is_reached(*target_cell.coordinates()):
            return g.backtrace_path(source_cell.coordinates(), target_cell.coordinates()) # backtrace path and do clean up


if __name__ == '__main__':

    filename_grid, filename_netlist = sys.argv[1:3]
    g = RoutingGrid.read_grid_from_file(filename_grid)
    nl = netlist.read_netlist_from_file(filename_netlist)
    for net in nl:
        net.path = maze_algorithm(g,net)
    netlist.write_output_file(filename_grid, nl)