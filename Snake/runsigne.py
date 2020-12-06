import random
from snake import SnakeGame

snake = SnakeGame()

class Node: 
    def __init__(self, position, move = None, parent = None):
        self.depth = 0
        self.h = 0
        self.cost = 0 
        if(parent):
            self.depth = parent.depth + 1
        self.position = position
        self.parent = parent
        self.move = move
        
    def move_list(self):
        moves = []
        aNode = self
        while aNode.parent:
            moves.append(aNode.move)
            aNode = aNode.parent
        moves.reverse()
        return moves

def getDistance(nodeOne, nodeTwo):
    return abs(nodeOne.position[0] - nodeTwo.position[0]) + abs(nodeOne.position[1] - nodeTwo.position[1])

def AStar(snake_head_position, apple_position):
    open_list = [Node(snake_head_position)]
    closed_list = []
   
    while(open_list):
        lowest_cost = 999999
        for aNode in open_list:
            if(aNode.cost < lowest_cost):
                lowest_cost = aNode.cost
                node = aNode

        open_list.remove(node)
        closed_list.append(node)
        for move in ['left', 'right', 'up', 'down']:
            new_pos = snake.simulate_move(node.position, move)
            child = Node(new_pos, move, node)
            if(not snake.is_legal(child.move_list())):
                continue
            if(child.position == snake.get_apple_position()):
                return child.move_list()
            for aNode in open_list:
                if(aNode.position == child.position and child.cost < aNode.cost):
                    open_list.remove(aNode)
            for aNode in closed_list:
                if(aNode.position == child.position and child.cost < aNode.cost):
                    closed_list.remove(aNode)

            child.h = getDistance(child, Node(snake.get_apple_position()))
            child.cost = child.h + child.depth
            open_list.append(child)
            

@snake.register_ai
def super_ai():
    res = AStar(snake.get_snake_head_position(), snake.get_apple_position())
    print(res)
    return res

snake.start(use_ai=True)



#snake = Environment()
#snake.printEnvironment()
#res = Astar(e.graph[0], e.graph[-1])
#snake.setWalked(res)
#print(res)
#snake.printEnvironment()

