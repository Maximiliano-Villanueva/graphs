from dotenv import load_dotenv
import sys
import os
import network
from graph import *


#load variables to env
curr_dir = os.path.dirname(os.path.realpath(__file__))
print('startint parser')
load_dotenv(os.path.join(curr_dir,'.env'))
data_dir = os.getenv("DATA_DIR")
out_dir = os.getenv("OUTPUT_DIR")

#assert path existance
if not os.path.exists(data_dir):
    raise Exception('input data dir does not exist')
    sys.exit()

if not os.path.exists(out_dir):
    raise Exception('out data dir does not exist')
    sys.exit()

print('loading data from: {0}'.format(data_dir))

try:

    test = Tm1Graph(data_path = data_dir)
    cubes = test.parseContent()

    nodes, green, red = test.getNodesAndEdges(cubes)

    net = network.CubeGraph(nodes, green, red)
    net.createAll()
    net.save_graph(os.path.join(out_dir,'test.png'))
except e:
    print (e)
    