import sys, os

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..','..')
sys.path.append(ROOT_DIR)
from src.network import *

import unittest

class MultiGraph(unittest.TestCase):

    def test_multi_edge_node(self):

        number_of_nodes = 6
        nodes = ['0000 very long and unique string number {}'.format(i) for i in range(0,number_of_nodes)]
        green = []
        red = []


        green.append(('0000 very long and unique string number 0', '0000 very long and unique string number 1'))
        red.append(('0000 very long and unique string number 1', '0000 very long and unique string number 0'))
        red.append(('0000 very long and unique string number 0', '0000 very long and unique string number 1'))
        red.append(('0000 very long and unique string number 0', '0000 very long and unique string number 1'))

        green.append(('0000 very long and unique string number 2', '0000 very long and unique string number 3'))
        red.append(('0000 very long and unique string number 3', '0000 very long and unique string number 2'))

        green.append(('0000 very long and unique string number 4', '0000 very long and unique string number 5'))
        red.append(('0000 very long and unique string number 5', '0000 very long and unique string number 4'))

        net = CubeGraph(nodes, green, red)
        net.createAll()
        save_path = os.path.join(ROOT_DIR, 'output', 'testedge.png')
        net.save_graph(save_path)
        
        self.assertGreater(os.path.getsize(save_path), 0)


unittest.main()