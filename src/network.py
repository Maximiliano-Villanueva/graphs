#from tkinter.ttk import Notebook
import networkx as nx
import matplotlib.pyplot as plt
import os

class Graph:
    """
    create and visualize a graph using networkx
    """
    def __init__(self, out_width = 200, out_height = 80):
        """
        basic constructor
        """
        
        self.G = nx.MultiDiGraph()
        self.IMAGE_WIDTH= out_width
        self.IMAGE_HEIGHT = out_height
        self.edgesColor = []
        self.edgesList = dict()


    def addNodes(self,nodes, options = {'color' : 'blue'}):
        """
        add nodes to the graph
        """
        #asserts
        if self.G is None:
            raise Exception('graph not created')
        if options is None:
            raise Exception('options  parameter is none type')
        if not isinstance(nodes, list):
            raise Exception('nodes parameter must be a list')

        #add nodes with options
        for n in nodes:
            opt = options
            opt['label'] = n
            
            self.G.add_nodes_from(
                [(n, opt)]
            )
            


    def addEdges(self, edges, options = {'color' : 'green'}):
        """
        add edges to the graph
        """
        #asserts
        if self.G is None:
            raise Exception('graph not created')
        if options is None: 
            raise Exception('options  parameter is none type')
        if not isinstance(edges, list):
            raise Exception('edges parameter must be a list')
        
        #add edges with options
        
        for n in edges:
            opt = options
            opt['label'] = n

            self.edgesColor.append(opt["color"])

            if not (n in self.edgesList.keys()):
                self.edgesList[n] = list()

            self.edgesList[n].append(opt['color'])
            self.G.add_edges_from(
                [n + (options,)]
            )
            

    
    def removeNodes(self, nodes):
        """
        remove nodes from graph
        """
        if self.G is None:
            raise Exception('graph not created')
        if not isinstance(nodes, list):
            raise Exception('nodes parameter must be a list')

        self.G.remove_nodes_from(nodes)

    def removeEdges(self,edges):
        """
        remove edges from graph
        """

        if self.G is None:
            raise Exception('graph not created')
        if not isinstance(edges, list):
            raise Exception('edges parameter must be a list')

        self.G.remove_edges_from(edges)
    
    def _prepareOutput(self):
        fig = plt.figure(1, figsize=(self.IMAGE_WIDTH, self.IMAGE_HEIGHT), dpi=60)
        ax = plt.gca()
        
        # Compute position of nodes
        pos = nx.kamada_kawai_layout(self.G, scale = 0.5)
        # Draw nodes and edges
        nx.draw_networkx_nodes(self.G, pos, labels = list(self.G.nodes), node_size=10000)
        nx.draw_networkx_labels(self.G, pos, {n: n for n in list(self.G.nodes)}, font_size=100)
        
        """
        nx.draw_networkx_edges(
            self.G, pos,
            connectionstyle="arc3,rad=0.1"
            ,edge_color = self.edgesColor
            ,arrowsize=20
        )
        """
        #nx.draw_networkx_edge_labels(self.G, pos, {n: n for n in list(self.G.edges)}, font_size=6)
        
        #keep max number of edges between nodes to calculate the rad later
        max_values = dict()
        for e in self.G.edges:
            if not((e[0], e[1]) in max_values.keys()):
                max_values[(e[0], e[1])] = len(self.edgesList[(e[0], e[1])])
                
            col = self.edgesList[(e[0], e[1])][-1]
            calc_rad = (len(self.edgesList[(e[0], e[1])]) / max_values[(e[0], e[1])])/2
            calc_rad = calc_rad if col == 'green' else calc_rad * (-1)
            ax.annotate("",
                xy=pos[e[0]], xycoords='data',
                xytext=pos[e[1]], textcoords='data',
                arrowprops=dict(arrowstyle="->", color=col,
                                shrinkA=5, shrinkB=5,
                                patchA=None, patchB=None,
                                connectionstyle="arc3,rad=rrr".replace('rrr',str(calc_rad)
                                ),
                                ),
            )
            self.edgesList[(e[0], e[1])].pop(),
    def plot(self):
        """
        plot graph
        """
        
        self._prepareOutput()
        plt.show()


    def save_graph(self, filename):
        """
        save graph to file
        """
        self._prepareOutput()
        
        fname=os.path.splitext(filename)[0]
        fname = fname[0:fname.rfind(os.path.sep)]
        if not os.path.exists(fname):
            raise Exception('directory: {0} does not exist or cannot be written'.format(fname))
        plt.savefig(filename)
        

class CubeGraph(Graph):
    """
    this class handles graphs for cubes
    """

    def __init__(self, nodes, green_edges, red_edges):
        """
        constructor for cube graph
        """
        #asserts
        if not isinstance(nodes, list):
            raise Exception('nodes parameter must be a list')
        if not isinstance(green_edges, list):
            raise Exception('green_edges parameter must be a list')
        if not isinstance(red_edges, list):
            raise Exception('red_edges parameter must be a list')

        #assign variables
        self._nodes = nodes
        self._greenEdges = green_edges
        self._redEdges = red_edges
        
        #init parent object
        super().__init__()

    def createAll(self):
        """
        create the graph with all the nodes and edges
        """
        self.addNodes(self._nodes)
        self.addEdges(self._greenEdges, {'color' : 'green'})
        self.addEdges(self._redEdges, {'color' : 'red'})

    def create(self, node):
        """
        create a graph only with related node
        """

        if node in self._nodes_:
            raise Exception('node parameter is not nodes list provided at initialization')
        #clean the graph
        self.removeEdges(self._redEdges)
        self.removeEdges(self._greenEdges)
        self.removeNodes(self._nodes)

        #make sure node is lower case
        node = node.lower()

        #filter only those edges matching the node
        green_filtered = list(filter(lambda x : x[0] == node, self._greenEdges))
        red_filtered = list(filter(lambda x : x[1] == node, self._redEdges))

        #add nodes and edges to graph
        self.addNodes(node)
        self.addEdges(green_filtered, {'color' : 'green'})
        self.addEdges(red_filtered, {'color' : 'red'})

