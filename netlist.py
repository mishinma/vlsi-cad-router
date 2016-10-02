from wavefront import WavefrontCell


class Net():
    """
    Class to specify nets
    NetID, LayerPin1, (Xpin1, Ypin1), LayerPin2, (Xpin2, Ypin2)
    """
    def __init__(self, net_id, layer_1id, x_1, y_1, layer_2id, x_2, y_2):

        self.id = net_id
        self.s = WavefrontCell(x_1, y_1, layer_1id-1)
        self.t = WavefrontCell(x_2, y_2, layer_2id-1)
        self.path = list()



def read_netlist_from_file(filename):
    with open(filename, 'rt') as f:
        net_number = int(f.readline())
        netlist = []
        for _ in range(net_number):
            netlist.append(Net(*[int(_) for _ in f.readline().split()]))  # Read line, initialize net, append net to the netlist
        return netlist


def write_output_file(input_filename, nl):
    """

    :param filename: filename.nl - name of the input file
    :param nl:
    :return:
    """
    output_filename = input_filename.split('.')[0] + '.out'
    with open(output_filename, 'wt') as f:
        f.write('{}\n'.format(len(nl)))

        for net in nl:
            f.write('{}\n'.format(net.id))
            for cell in net.path:
                f.write('{} {} {}\n'.format(cell[2]+1, cell[0], cell[1]))  # layer+1 x y
            f.write('0\n')





