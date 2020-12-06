import random
from snake import SnakeGame

snake = SnakeGame()
debug=False
moves=['up', 'down', 'left', 'right']

class Node:
    def __init__(self,position,move=None,parent=None):
        self.position = position
        self.move = move
        self.parent=parent
        self.depth=0
        if(parent):
            self.depth = parent.depth + 1
        self.h=0
        self.cost=0
    
    def getPath(self):
        moves = []
        aNode=self  
        while(aNode.parent):
            moves.append(aNode.move)
            aNode = aNode.parent
        moves.reverse()
        return moves

    def describe(self):
        print("Node@: {0}, Move: {1}, Parent@: {2}, Depth, h & cost: {3}, {4}, {5}".format(self.position,self.move,self.parent.position,self.depth,self.h,self.cost))

def getDistance(nodeOne, nodeTwo):
    return abs(nodeOne.position[0] - nodeTwo.position[0]) + abs(nodeOne.position[1] - nodeTwo.position[1])

def aStar(start,stopp):
    openlist=[start]
    closedlist=[]
    runde=0
    while(openlist):
        runde+=1
        compare = 100
        for node in openlist:
            if(node.cost<compare):
                compare = node.cost
                aNode=node

        if not debug:
            openlist.remove(aNode)
            closedlist.append(aNode)
        else:
            try:
                print("Node@: {0}, Move: {1}, Parent@: {2}, Depth, h & cost: {3}, {4}, {5}".format(aNode.position,aNode.move,aNode.parent.position,aNode.depth,aNode.h,aNode.cost))
                openlist.remove(aNode)
                closedlist.append(aNode)
            except:
                a=2 #Placeholder so empty except won't raise error
        for move in moves:
            child = Node(snake.simulate_move(aNode.position,move),move,aNode)
            if(not snake.is_legal(child.getPath())):
                continue
            if(child.position==stopp.position):
                return child.getPath()
            for aNode in openlist:
                if(aNode.position == child.position and child.cost < aNode.cost):
                    openlist.remove(aNode)
            for aNode in closedlist:
                if(aNode.position == child.position and child.cost < aNode.cost):
                    closedlist.remove(aNode)
            child.h = getDistance(child,stopp)
            child.cost=child.depth+child.h
            openlist.append(child)
           
@snake.register_ai
def super_ai():
    hNode = Node(snake.get_snake_head_position())
    apNode = Node(snake.get_apple_position())
    moves = aStar(hNode,apNode)
    return moves

snake.start(use_ai=True)