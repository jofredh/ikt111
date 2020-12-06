import random
import copy

class NodeTicTacToe:
    def __init__(self,position):
        self.move = "."
        self.position = position
        self.heuristic = 0
        

P1 = "X"
P2 = "O"

class EnvTicTacToe:
    def __init__(self):
        self.nodes = []
        self.stop = False
        for x in range(0,3):
            for y in range(0,3):
                n = NodeTicTacToe([x,y])
                self.nodes.append(n)

    def findNode(self,x,y,nodes):
        for aNode in nodes:
            if(aNode.position[0]==x and aNode.position[1]==y):
                return aNode

    def printBoard(self,nodes,positions=False):
        print()
        for x in range(0,3):
            for y in range(0,3):
                print(self.findNode(x,y,nodes).move,end=" ")
            print()
        print()
        if positions:
            for x in range(0,3):
                for y in range(0,3):
                    print(self.findNode(x,y,nodes).position,end=" ")
                print()
            print()




    def heuristic(self,nodes):
        points_p1_x = {}
        points_p1_y = {}
        points_p2_x = {}
        points_p2_y = {}
        for aNode in nodes:
            if(aNode.move==P1): #P1
                points_p1_x[aNode.position[0]] = points_p1_x.get(aNode.position[0],0)+1
                points_p1_y[aNode.position[1]] = points_p1_y.get(aNode.position[1],0)+1
            if(aNode.move==P2): #P2
                points_p2_x[aNode.position[0]] = points_p2_x.get(aNode.position[0],0)+1
                points_p2_y[aNode.position[1]] = points_p2_y.get(aNode.position[1],0)+1
        p1points = max(list(points_p1_x.values()) + list(points_p1_y.values()) + [0])
        p2points = max(list(points_p2_x.values()) + list(points_p2_y.values()) + [0])
        h = (p2points-p1points)*10
        if(p2points==3):
            h = 100
        if(p1points==3):
            h = -100
        
        h = h-len(self.getAllFree(nodes))
        return h,p1points,p2points

    def is_full(self,nodes):
        num_empty = len([i for i in nodes if i.move=="."])
        if(num_empty==0):
            return True
        else:
            return False

    def getAllFree(self,nodes):
        all_free_nodes = []
        for aNode in nodes:
            if aNode.move==".":
                all_free_nodes.append(aNode)
        random.shuffle(all_free_nodes)
        return all_free_nodes


    def is_winning(self,nodes):
        h,p1points,p2points = self.heuristic(nodes)
        if(p1points==3):
            return P1
        if(p2points==3):
            return P2
        return False

    def p2_simple(self):
        move = " "
        while (not move=="."):
            aNode = random.choice(self.nodes)
            move = aNode.move
        aNode.move = "O"
    
    def p2_minimax(self):
        node = self.minimax(self.nodes,True,0,None)
        aNode = self.findNode(node.position[0],node.position[1],self.nodes)
        aNode.move = P2 #O

    def minimax(self,nodes,maximize,counter,parent):
        if(counter>3 or self.is_full(nodes)):
            parent.heuristic = self.heuristic(nodes)[0]
            return parent
        all_free_nodes = self.getAllFree(nodes)
        branches = []
        for aNode in all_free_nodes:
            nodes_new = copy.deepcopy(nodes)
            aNode = self.findNode(aNode.position[0],aNode.position[1],nodes_new)
            if(maximize):
                aNode.move = P2
                aNode.heuristic = -100000
                subnode = self.minimax(nodes_new, not maximize,counter +1, aNode)
                aNode.heuristic = max([node.heuristic for node in [aNode,subnode] if node])
            else:
                aNode.move = P1
                aNode.heuristic = 100000
                subnode = self.minimax(nodes_new, not maximize,counter +1, aNode)
                aNode.heuristic = min([node.heuristic for node in [aNode,subnode] if node])
            branch = aNode
            branches.append(branch)
        if(maximize):
            one_heuristic = max([i.heuristic for i in branches])
        else:
            one_heuristic = min([i.heuristic for i in branches])
        all_with_correct_heuristic = [i for i in branches if i.heuristic==one_heuristic]
        bestNode = random.choice(all_with_correct_heuristic)
        return bestNode



e = EnvTicTacToe()
e.printBoard(e.nodes,True)

while((not e.is_winning(e.nodes)) and (not e.is_full(e.nodes))):
    x,y = input("Skriv X og Y med mellomrom:").split(" ")
    x = int(x)
    y = int(y)
    e.findNode(x,y,e.nodes).move = "X"
    #e.p2_simple()
    e.p2_minimax()
    e.printBoard(e.nodes,True)

#while((not e.is))
