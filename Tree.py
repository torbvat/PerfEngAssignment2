""" 
Created by: Torbjørn Vatne and Erlend Nygaard Kristiansen
Group 18
"""
import DatabaseHandler

# Nodes
# --------
class Node:
    def __init__(self, move, plyCount=0, nodeID=0):
        self.name = move.getMoveText() if not plyCount == 0 else "Root"
        self.resultCounts = {
            'white_wins': 0,
            'black_wins': 0,
            'draws': 0,
        }
        self.children = []
        self.plyCount = plyCount
        self.whitePlayer = True if int(self.plyCount) % 2 == 1 else False
        self.nodeID = nodeID

    def getName(self):
        return self.name

    def getPlyCount(self):
        return self.plyCount

    def getID(self):
        return self.nodeID

    def getResultCounts(self):
        return self.resultCounts

    def getGamesPlayed(self):
        return sum(self.resultCounts.values())

    def getChildren(self):
        return self.children

    def isWhitePlayer(self):
        return self.whitePlayer

    def __repr__(self):
        return (f"|{self.name} : {self.plyCount} : {len(self.children)}|")
# Edges
# --------
class Edge:
    def __init__(self, sourceNode, targetNode):
        self.sourceNode = sourceNode
        self.targetNode = targetNode

    def getSourceNode(self):
        return self.sourceNode

    def getTargetNode(self):
        return self.targetNode

# Trees
# ---------
class Tree:
    def __init__(self, games):
        self.edges = []
        self.games = games
        self.root = Node("", 0, 0)
        self.nodes = [self.root]
        self.nodeID = 1

    def getID(self):
        return self.nodeID

    def setRootName(self, name):
        self.root.name = name

    def increaseID(self):
        self.nodeID += 1

    def getNodes(self):
        return self.nodes

    def getEdges(self):
        return self.edges

    def getRoot(self):
        return self.root

    def newNode(self, move, plyCount, currentNode, winner):
        newNode = Node(move, plyCount, self.getID())
        newNode.resultCounts[winner] += 1
        self.nodes.append(newNode)
        self.edges.append(Edge(currentNode, newNode))
        self.increaseID()
        return newNode

# Printer
# ----------
class Printer:
    def __init__(self):
        pass

    def lookForNodeInChildren(self, moveName, children):
        for node in children:
            if node.getName() == moveName:
                return node
        return None

    # Writes the tree to a file in the DOT language
    def writeTreeToDotFile(self, tree, filePath, depth=10, threshold=1):
        if threshold < 1 or depth < 1:
            raise ValueError("Threshold and depth must be greater than 0")
        with open(filePath, 'w') as file:
            file.write("graph ChessOpenings {\n")
            file.write('\trankdir="LR";\n')
            root = tree.getRoot()

            # Adds up the result counts of all the children of the root node
            for i in range(0, len(tree.getRoot().getChildren())):
                tree.getRoot().getResultCounts()["white_wins"] += tree.getRoot().getChildren()[i].getResultCounts()['white_wins']
                tree.getRoot().getResultCounts()["black_wins"] += tree.getRoot().getChildren()[i].getResultCounts()['black_wins']
                tree.getRoot().getResultCounts()["draws"] += tree.getRoot().getChildren()[i].getResultCounts()['draws']
           
            # Writes the nodes to the file if they have been played more than 'threshold' times and are 'depth' moves deep
            for node in tree.getNodes():
                if (node.getGamesPlayed() > threshold) and (node.getPlyCount() <= depth):
                    if node.isWhitePlayer():
                        file.write(f"\t{node.getID()} [label = \"{node.getName()}\nWhite:{node.getResultCounts()['white_wins']}\nDraws:{node.getResultCounts()['draws']}\nBlack:{node.getResultCounts()['black_wins']}\"]; \n")
                    else:
                        file.write(
                            f"\t{node.getID()} [label = \"{node.getName()}\nWhite:{node.getResultCounts()['white_wins']}\nDraws:{node.getResultCounts()['draws']}\nBlack:{node.getResultCounts()['black_wins']}\", style = filled, fillcolor = black, fontcolor = white]; \n")
            
            # Writes each edge to the file if the target node has been played more than 'threshold' times and is 'depth' moves deep
            for edge in tree.getEdges():
                if (edge.getTargetNode().getGamesPlayed() > threshold) and (edge.getTargetNode().getPlyCount() <= depth):
                    file.write(f"\t{edge.getSourceNode().getID()} -- {edge.getTargetNode().getID()};\n")
            
            # Writes the root node to the file
            file.write(f"\t{root.getID()} [label = \"{root.getName()}\nWhite:{root.getResultCounts()['white_wins']}\nDraws:{root.getResultCounts()['draws']}\nBlack:{root.getResultCounts()['black_wins']}\", shape = octagon, style = filled, fillcolor = darkgreen, fontcolor = black]; \n")
            file.write("}")

    # Gets all the games with a certain opening
    def getGamesWithOpening(self, games, opening):
        relevantGames = []
        for game in games:
            if game.getOpening() == opening:
                relevantGames.append(game)
        if relevantGames == []:
            raise ValueError("No games with that opening")
        return relevantGames


    # Creates a tree of the first 'maxSteps' moves of each game given in the constructor
    def createTree(self, games, filePath, maxSteps=500, minAmountOfGames=1):
        if maxSteps < 1:
            raise ValueError("Max steps must be greater than 0")
        
        tree = Tree(games)
        tree.setRootName(games[0].getOpening())
        for game in games:
            if game.getResult() == "1-0":
                winner = "white_wins"
            elif game.getResult() == "0-1":
                winner = "black_wins"
            else:
                winner = "draws"
            current_node = tree.getRoot()
            current_depth = 0

            #Iterate through the moves of the game until the max depth is reached or the end of the game is reached
            for move in game.getMoves()[:maxSteps] if maxSteps < len(game.getMoves()) else game.getMoves():
                next_node = self.lookForNodeInChildren(move.getMoveText(), current_node.getChildren())
                if next_node: #If the node already exists, just increment the result count and move on
                    next_node.getResultCounts()[winner] += 1
                    current_node = next_node 
                    current_depth += 1
                else:
                    break #If the node doesn't exist, break out of the loop and create the rest of the nodes (loop below)
            
            for move in game.getMoves()[current_depth:maxSteps] if maxSteps < len(game.getMoves()) else game.getMoves()[current_depth:]:  
                new_node = tree.newNode(move, current_depth+1, current_node, winner) 
                current_node.children.append(new_node)
                current_node = new_node
                current_depth += 1
        self.writeTreeToDotFile(tree, filePath, maxSteps, minAmountOfGames)
        return tree

    # Writes a tree of the games with a certain opening to a DOT-file
    def createTreeWithOpening(self, filePath, opening, games, depth=500, threshold=1):
        if depth < 1 or threshold < 1:
            raise ValueError("Depth and threshold must be greater than 0")
        relevantGames = self.getGamesWithOpening(games, opening)
        self.createTree(relevantGames, filePath, depth, threshold)
        return filePath

#DE TO NEDERSTE METODENE SKAL TAS I BRUK I MAIN (SLETT KOMMENTAR)