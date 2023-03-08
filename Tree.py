#Graphs

# 1. Imported Modules
# -------------------
from graphviz import Digraph
import DatabaseHandler
import os
# 2. Nodes
# --------


class Node:
    def __init__(self, move, ply_count=0):
        self.name = move.get_move_text() if not ply_count == 0 else "Root"
        self.meta = {
            'white_wins': 0,
            'black_wins': 0,
            'draws': 0,
        }
        self.children = []
        self.ply_count = ply_count
        self.white_player = True if int(self.ply_count) % 2 == 1 else False

    def getName(self):
        return self.name

    def getMoveNumber(self):
        return self.ply_count

    def isWhitePlayer(self):
        return self.white_player

    def getWhiteWins(self):
        return self.meta['white_wins']

    def getBlackWins(self):
        return self.meta['black_wins']

    def getDraws(self):
        return self.meta['draws']

    def getChildren(self):
        return self.children

    def increaseWhiteWins(self):
        self.meta['white_wins'] += 1

    def increaseBlackWins(self):
        self.meta['black_wins'] += 1

    def increaseDraws(self):
        self.meta['draws'] += 1

    def __repr__(self):
        return (f"|{self.name} : {self.ply_count} : {len(self.children)}|")
# 3. Edges
# --------


class Edge:
    def __init__(self, sourceNode, targetNode):
        self.sourceNode = sourceNode
        self.targetNode = targetNode
        self.weight = 1  # Number of times a game has this opening

    def getSourceNode(self):
        return self.sourceNode

    def getTargetNode(self):
        return self.targetNode

    def getWeight(self):
        return self.weight

    def increaseWeight(self):
        self.weight += 1

# 4. Graphs
# ---------


class Graph:
    def __init__(self, games):
        #self.move_counter = 0
        
        self.edges = []
        self.games = games
        self.root = Node("", 0)
        self.nodes = [self.root]
    # def lookForNode(self, move, previousMoves):
    #     for node in self.nodes:
    #         if node.getName() == move.get_move_text() and node.getMoveNumber() == self.move_counter and node.getPreviousMoves == previousMoves:
    #             return node
    #     return None

    def lookForEdge(self, sourceNode, targetNode):
        for edge in self.edges:
            if edge.getSourceNode() == sourceNode and edge.getTargetNode() == targetNode:
                return edge
        return None

    def newNode(self, move, ply_count):
        if move not in self.nodes[ply_count-1].children:
            self.nodes[-1].children.append(move)
            self.nodes.append(Node(move, ply_count))
            self.edges.append(Edge(self.nodes[ply_count-1], self.nodes[ply_count]))
        #else:
        #    for edge in self.edges:
        #        if edge.getSourceNode() == self.nodes[ply_count-1] and edge.getTargetNode().getName() == move.get_move_text():
        #            edge.increaseWeight()
            
            #self.nodes[ply_count].increaseWhiteWins() if self.nodes[ply_count].isWhitePlayer() else self.nodes[ply_count].increaseBlackWins()
            #self.nodes[ply_count].increaseDraws() if self.nodes[ply_count].isWhitePlayer() else self.nodes[ply_count].increaseDraws()


    def getNodes(self):
        return self.nodes.values()

    def getEdges(self):
        return self.edges

    def longestGame(self, games):
        longest = 0
        for game in games:
            if len(game.moves) > longest:
                longest = len(game.moves)
        return longest

# 5. Printer
# ----------


class Printer:
    def __init__(self, games):
        self.games = games

    def createGraph(self):
        graph = Graph(self.games)
        for game in self.games:
            ply_count = 1
            for move in game.get_moves():
                graph.newNode(move, ply_count)
                ply_count += 1
        return graph

    def exportGraph(self, fileName):
        graph = self.createGraph()
        with open(fileName, "w") as f:
            self.printGraph(graph, f)

    def printGraph(self, outputFile):
        graph = self.createGraph()
        outputFile.write("graph {0:s}\n".format(graph.getName()))
        for node in graph.getNodes():
            self.printNode(node, outputFile)
        for edge in graph.getEdges():
            self.printEdge(edge, outputFile)
        outputFile.write("end\n")

    def printNode(self, node, outputFile):
        outputFile.write("\tnode {0:s}\n".format(node.getName()))

    def printEdge(self, edge, outputFile):
        sourceNode = edge.getSourceNode()
        targetNode = edge.getTargetNode()
        weight = edge.getWeight()
        outputFile.write("\tedge ")
        outputFile.write(sourceNode.getName())
        outputFile.write(" ")
        outputFile.write(targetNode.getName())
        outputFile.write(" ")
        outputFile.write("{0:f}".format(weight))
        outputFile.write("\n")

# 6. Reader
# ---------


class Reader:
    def __init__(self):
        pass

    def importGraph(self, fileName):
        inputFile = open(fileName, "r")
        graph = self.readGraph(inputFile)
        inputFile.close()
        return graph

    def readGraph(self, inputFile):  # Skriv om hele denne metoden
        tokens = self.readTokens(inputFile)
        name = tokens[1]
        graph = Graph(name)
        index = 2
        while index < len(tokens):
            token = tokens[index]
            if token == "node":
                nodeName = tokens[index+1]
                graph.newNode(nodeName,)
                index += 2
            elif token == "edge":
                sourceNodeName = tokens[index+1]
                targetNodeName = tokens[index+2]
                weightString = tokens[index+3]
                sourceNode = graph.lookForNode(sourceNodeName)
                targetNode = graph.lookForNode(targetNodeName)
                weight = float(weightString)
                graph.newEdge(sourceNode, targetNode, weight)
                index = index + 4
            elif token == "end":
                break
        return graph

    def readTokens(self, inputFile):
        tokens = []
        for line in inputFile:
            line = line.strip()
            self.readTokensInLine(line, tokens)
        return tokens

    def readTokensInLine(self, line, tokens):
        lineTokens = line.split()
        tokens.extend(lineTokens)

# 7. Main
# -------


# printer = Printer()

# game_reader = DatabaseHandler.DatabaseHandler("Datafiles\StockfishShort.pgn")
# games = game_reader.read_games()
# network = Graph("MyNet")
# network.setNodes(games)
# printer.exportGraph(network, "Datafiles\MyNet.txt")
# printer = Printer()

# reader = Reader()
# graph = reader.importGraph("Datafiles\MyNet.txt")
# printer.exportGraph(graph, "Datafiles\MyNet2.txt")


"""
digraph SLETTMyNet {
	A -> B [label=10];
	A -> C [label=12];
	B -> C [label=5];
	B -> D [label=8];
	C -> D [label=2];
}
"""

# [e4, e5, d5, c6]
# for game in games:
#     teller
#     node1 = Node(e4, teller, teller mod 2, previousMoves)


# lookForNode(move, moveCount, previousMoves[])
# createNewNode(move, moveCount, previousMoves[]). Oppretter en edge fra siste node i previousMoves til denne.
# addNode
# if lookfornode
#increaseWeight(node, node.previousMoves[-1])