# Impplementation using anytree library
# To install the anytree module run:
#    pip install anytree

from anytree import Node, NodeMixin, RenderTree
import math
from .jogo_back import JogoBack

class BaseTree(object):  # Just an example of a base class
    pass

class Tree(BaseTree, NodeMixin):  # Add Node feature
    def __init__(self, score_sum, parent=None, children=None):
        super(Tree, self).__init__()
        self.score_sum = score_sum
        self.visit_count = 0
        self.current_board_stage = None
        self.parent = parent
        if children:
           self.children = children

    def get_avarage(self):
        return (self.score_sum/self.visit_count)

    def ucb1(self):
        if(self.visit_count == 0):
            return math.inf
        return (self.get_avarage() + 2*(math.sqrt(math.log10(self.parent.score_sum)/self.visit_count)))

    def select_node(self): #choses the best node based on the Upper Confidence Bound (UCB1)

        max = 0.0
        var = self
        while var.is_leaf == False:
            for node in var.children:
                if node.ucb1() > max:
                    max = node.ucb1()
                    var = node
        return var

    def back_propagation(self, score): #after a simulation, back propagates the new values
        if(self.parent != None):
            self.parent.score_sum += score
            self.parent.visit_count += 1
            self.parent.back_propagation(score)

def simulate(self, node): #I.A.'s work: simulate the game to return a stage game with its datas
    self.node = node
    return node

def expand(self, node): #I.A.'s work
    self.node = node
    return node

def MCTS(tree):

    node = tree.select_node()

    if node.is_leaf: #the node is a leaf: we need to find out its situation(bad or good)
        result = simulate(node) #A.I. will simulate and give a score to the node
        node.back_propagation(result.score_sum)
        return tree.root
    #the node has alredy been visited: we can expand it by giving new stages(moves in the game)
    node.children = expand(node) #expands the current node
    result = node.select_node() #selects the best node to be simulated
    result = simulate(result)
    result.back_propagation(result.score_sum)
    return tree.root

def generateTree(num_iterations):
    tree = tree(0)
    for _ in range(num_iterations):
         tree = MCTS(tree)
    return tree