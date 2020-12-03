# Impplementation using anytree library
# To install the anytree module run:
#    pip install anytree

import time
from anytree import Node, NodeMixin, RenderTree
import math
from copy import copy, deepcopy
from random import seed
from random import randint

  
class BaseTree(object):  # Just an example of a base class
    pass

class Tree(BaseTree, NodeMixin):  # Add Node feature

    def __init__(self, parent=None, children=None):
        super(Tree, self).__init__()
        self.score = 0
        self.visits = 0
        self.currente_board = None #stores the state of the game
        self.parent = parent
        self.terminal = False #terminal: win, lose, draw
        #self.player = 0
        if children:
            self.children = children

    ################
    #MCTS FUNCTIONS
    ################

    def ucb1(self):

        if(self.visits == 0):
            return math.inf
        return ((self.score/self.visits) + math.sqrt(2 * math.log10(self.parent.visits)/self.visits))

    def select_node(self): #choses the best node based on the Upper Confidence Bound (UCB1)

        max = -math.inf
        var = self
        best_node = None

        while var.is_leaf == False:

            for node in var.children:
                if node.ucb1() > max:
                    max = node.ucb1()
                    best_node = node
            var = best_node
            max = -math.inf

        return var

    def back_propagation(self, score): #after a simulation, back propagates the new values: visit and score

        if(self.parent != None):
            self.parent.score += score
            self.parent.visits += 1
            self.parent.back_propagation(score)

    def expand(self): #I.A.'s work
        #Must return the possible children (actions) and define which of then is a terminal(end, win, draw)
        #Deve retornar os filhos (ações) possíveis e informar se são terminais
        # terminais são estados de vitória ou derrota
    
    def simulate(self): #I.A.'s work: simulate the game to return a stage game with its datas
        
        #must simulate the game state of the node and return its score


    def get_best_child_by_visits(self): #selects the most visited child

        max = 0
        var = None
        for node in self.root.children:
            if node.visits > max:
                max = node.visits
                var = node
        return var

    def get_best_child_by_ucb(self): #selectes the child that has the highest UBB value

        max = -math.inf
        best_child = None

        for node in self.root.children:
            if node.ucb1() > max:
                max = node.ucb1()
                best_child = node

        return best_child

def MCTS(tree): #creates the MCTS
    
    leaf = tree.root.select_node()

    if leaf.visits == 0 or leaf.terminal:
        leaf.score = leaf.simulate()
        leaf.visits = 1
        leaf.back_propagation(leaf.score)
        return leaf.root
        
    leaf.children = leaf.expand()  
    best_leaf_child = leaf.get_best_child_by_ucb()
    best_leaf_child.score = best_leaf_child.simulate()
    best_leaf_child.visits = 1
    best_leaf_child.back_propagation(best_leaf_child.score)

    return leaf.root



def get_best_action(board, num_iterations): # Returns the most promissing action in the game

    tree = deepcopy(board)    
    tree.children = tree.expand()

    for _ in range(num_iterations):
        tree = MCTS(tree)

    return tree.get_best_child_by_visits().currente_board
