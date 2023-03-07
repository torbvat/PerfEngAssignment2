# Graphs

# 1. Imported Modules
# -------------------
from graphviz import Digraph
import DatabaseHandler
import os
# 2. Nodes
# --------

class Node:
    white = "White"
    black = "Black"
    def __init__(self, name, player, move_number):
        self.name = name
        self.meta = {
            'white_wins': 0,
            'black_wins': 0,
            'draws': 0,
        }
        self.children = []
        self.parents = []
        self.player = player
        self.move_number = move_number


    def getName(self):
        return self.name
    
    def getPlayer(self):
        return self.player
    
    def getWhiteWins(self):
        return self.meta['white_wins']
    
    def getBlackWins(self):
        return self.meta['black_wins']
    
    def getDraws(self):
        return self.meta['draws']
    
    def getChildren(self):
        return self.children
    
    def getParents(self):
        return self.parents
    
    def increaseWhiteWins(self):
        self.meta['white_wins'] += 1

    def increaseBlackWins(self):
        self.meta['black_wins'] += 1

    def increaseDraws(self):
        self.meta['draws'] += 1
    
# 3. Edges
# --------

class Edge:
    def __init__(self, sourceNode, targetNode, depth):
        self.sourceNode = sourceNode
        self.targetNode = targetNode
        self.weight = 1 #Number of times a game has this opening
        self.depth = depth

    def getSourceNode(self):
        return self.sourceNode
    
    def setSourceNode(self, sourceNode):
        self.sourceNode = sourceNode

    def getTargetNode(self):
        return self.targetNode
    
    def setTargetNode(self, targetNode):
        self.targetNode = targetNode

    def getWeight(self):
        return self.weight
    
    def increaseWeight(self):
        self.weight += 1

# 4. Graphs
# ---------

class Graph:
    def __init__(self, name):
        self.name = name
        self.nodes = dict()
        self.edges = []
        self.games = games
        

    def getName(self):
        return self.name
    
    def setName(self, newName):
        self.name = newName

    def lookForNode(self, name):
        return self.nodes.get(name, None)

    def newNode(self, name, player):
        node = Node(name, player)
        self.nodes[name] = node
        return node

    def getNodes(self):
        return self.nodes.values()

    def newEdge(self, sourceNode, targetNode, depth):
        edge = Edge(sourceNode, targetNode, depth)
        if edge in self.edges:
            edge.increaseWeight()
        else:
            self.edges.append(edge)
        return edge

    def getEdges(self):
        return self.edges

    def longestGame(self, games):
        longest = 0
        for game in games:
            if len(game.moves) > longest:
                longest = len(game.moves)
        return longest

    def setNodes(self, games):
        move_count = 1
        #for i in range(self.longestGame(games)):
        for i in range(10):
            move_count += 1
            for game in games:
                if move_count % 2 == 0:
                    player = Node.black
                else:
                    player = Node.white
                if i < len(game.moves):
                    move = game.moves[i]
                    sourceNode = self.lookForNode(move.get_move_text())
                    if sourceNode==None:
                        sourceNode = self.newNode(move.get_move_text(), player)
                    if i+1 < len(game.moves):
                        move = game.moves[i+1]
                        targetNode = self.lookForNode(move.get_move_text())
                        if targetNode==None:
                            targetNode = self.newNode(move.get_move_text(), player)
                        self.newEdge(sourceNode, targetNode, move_count)

# 5. Printer
# ----------

class Printer:
    def __init__(self):
        pass

    def exportGraph(self, graph, fileName):
        with open(fileName, "w") as f:
            self.printGraph(graph, f)

    def printGraph(self, graph, outputFile):
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
    
    def printGraphViz(self, graph, fileName): #Kan sikkert slette
        dot = Digraph(comment=graph.getName())
        for node in graph.getNodes():
            dot.node(node.getName())
        for edge in graph.getEdges():
            sourceNode = edge.getSourceNode()
            targetNode = edge.getTargetNode()
            weight = edge.getWeight()
            dot.edge(sourceNode.getName(), targetNode.getName(), str(weight))
        dot.render(fileName, view=True)
    
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

    def readGraph(self, inputFile): #Skriv om hele denne metoden
        tokens = self.readTokens(inputFile)
        name = tokens[1]
        graph = Graph(name)
        index = 2
        while index<len(tokens):
            token = tokens[index]
            if token=="node":
                nodeName = tokens[index+1]
                graph.newNode(nodeName,)
                index += 2
            elif token=="edge":
                sourceNodeName = tokens[index+1]
                targetNodeName = tokens[index+2]
                weightString = tokens[index+3]
                sourceNode = graph.lookForNode(sourceNodeName)
                targetNode = graph.lookForNode(targetNodeName)
                weight = float(weightString)
                graph.newEdge(sourceNode, targetNode, weight)
                index = index + 4
            elif token=="end":
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

printer = Printer()

game_reader = DatabaseHandler.DatabaseHandler("Datafiles\StockfishShort.pgn")
games = game_reader.read_games()
network = Graph("MyNet")
network.setNodes(games)
printer.exportGraph(network, "Datafiles\MyNet.txt")
printer = Printer()

reader = Reader()
graph = reader.importGraph("Datafiles\MyNet.txt")
printer.exportGraph(graph, "Datafiles\MyNet2.txt")
