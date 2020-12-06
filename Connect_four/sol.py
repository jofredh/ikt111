import connect_four
from connect_four import ConnectFour
from connect_four import Node
import random
import time
game = ConnectFour()



class Node:
    def __init__(self, move, parent):
        self.move = move
        self.value = "."
        self.parent = parent
        self.heuristic = 0
        if not parent:
            self.depth = 1
            self.is_p2 = False
        else:
            self.depth = parent.depth + 1
            self.is_p2 = not parent.is_p2

    def move_list(self):
        moves = []
        node = self
        while node:
            moves.append((node.move, game.player1 if not node.is_p2 else game.player2))
            node = node.parent
        moves.reverse()
        return moves

    def root_move(self):
        node = self
        while node.parent:
            node = node.parent
        return node.move

def p1_random():
    nodes = random_game(False,0,None,None)
    print("Positions:",[aNode.move for aNode in nodes])
    print("Heuristic:",[aNode.heuristic for aNode in nodes])
    print("Depth:",[aNode.depth for aNode in nodes])
    print("P2:",[aNode.is_p2 for aNode in nodes])
    return nodes[0].move


def random_game(p2,counter,parent,state):
    # Sets max depth
    if(counter > 3):
        return []

    # Init branches
    branches = [] 

    # Get all valid cols
    for valid_col in game.get_all_valid_cols(state):
        # Create new node for each col
        aNode = Node(valid_col, parent)
        moves = aNode.move_list()
        state = game.simulate_moves(moves)

        # Check for winning states
        if(not p2 and game.is_winner(game.player1,state)):
            aNode.heuristic=1000
            return [aNode]

        if(p2 and game.is_winner(game.player2,state)):
            aNode.heuristic=-1000
            return [aNode]
        
        # Calculate score for node 
        aNode.heuristic = game.get_heuristic(state)

        # Branch recursively
        subbranch = random_game(not p2, counter + 1, aNode, state)

        # Exit point after recursive search
        branch = [aNode] + subbranch
        
        if subbranch:
            # Will only run if not at bottom
            aNode.heuristic = max([n.heuristic for n in branch]) 
            branches.append(branch)
        else:
            # Will only run _if_ at bottom
            branches.append([aNode])
    
    # Find highest score in all branches
    one_heuristic = max([n[0].heuristic for n in branches])

    # Create a list of all branches where score is equal to highest score
    all_with_correct_heuristic = [n for n in branches if n[0].heuristic==one_heuristic]

    # Return random branch from branches
    #branch = random.choice(branches)
    branch = random.choice(all_with_correct_heuristic)
    return branch


@game.register_ai
def super_ai():
    time.sleep(0.1)
    return p1_random()#p2_dfs()
game.start(use_ai=True)