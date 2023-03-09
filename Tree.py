# Graphs

# 1. Imported Modules
# -------------------
#from graphviz import Digraph
import DatabaseHandler
#import os
# 2. Nodes
# --------


class Node:
    def __init__(self, move, ply_count=0, nodeID=0):
        self.name = move.get_move_text() if not ply_count == 0 else "Root"
        self.meta = {
            'white_wins': 0,
            'black_wins': 0,
            'draws': 0,
        }
        self.children = []
        self.ply_count = ply_count
        self.white_player = True if int(self.ply_count) % 2 == 1 else False
        self.nodeID = nodeID

    def getName(self):
        return self.name

    def getMoveNumber(self):
        return self.ply_count

    def getGamesPlayed(self):
        return self.meta['white_wins'] + self.meta['black_wins'] + self.meta['draws']

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
        self.root = Node("", 0, 0)
        self.nodes = [self.root]
        self.nodeID = 1
    # def lookForNodeInChildren(self, move, previousMoves):
    #     for node in self.nodes:
    #         if node.getName() == move.get_move_text() and node.getMoveNumber() == self.move_counter and node.getPreviousMoves == previousMoves:
    #             return node
    #     return None

    def lookForEdge(self, sourceNode, targetNode):
        for edge in self.edges:
            if edge.getSourceNode() == sourceNode and edge.getTargetNode() == targetNode:
                return edge
        return None

    def newNode(self, move, ply_count, currentNode, winner):
        newNode = Node(move, ply_count, self.nodeID)
        newNode.meta[winner] += 1
        self.nodes.append(newNode)
        self.edges.append(Edge(currentNode, newNode))
        self.nodeID += 1

        # else:
        #    for edge in self.edges:
        #        if edge.getSourceNode() == self.nodes[ply_count-1] and edge.getTargetNode().getName() == move.get_move_text():
        #            edge.increaseWeight()

        #self.nodes[ply_count].increaseWhiteWins() if self.nodes[ply_count].isWhitePlayer() else self.nodes[ply_count].increaseBlackWins()
        #self.nodes[ply_count].increaseDraws() if self.nodes[ply_count].isWhitePlayer() else self.nodes[ply_count].increaseDraws()
        return newNode

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

    def lookForNodeInChildren(self, move_name, children):
        for node in children:
            if node.getName() == move_name:
                return node
        return None

    def createGraph(self, maxSteps):
        graph = Graph(self.games)
        for game in self.games:
            if game.get_result() == "1-0":
                winner = "white_wins"
            elif game.get_result() == "0-1":
                winner = "black_wins"
            else:
                winner = "draws"

            currentNode = graph.root
            currentDepth = 0
            for move in game.get_moves()[:maxSteps]:
                nextNode = self.lookForNodeInChildren(
                    move.get_move_text(), currentNode.children)
                if nextNode:
                    nextNode.meta[winner] += 1
                    #edge = graph.lookForEdge(currentNode, nextNode)
                    # edge.increaseWeight()
                    currentNode = nextNode
                    currentDepth += 1
                else:
                    break
            for move in game.get_moves()[currentDepth:maxSteps]:
                newNode = graph.newNode(
                    move, currentDepth+1, currentNode, winner)
                currentNode.children.append(newNode)
                currentNode = newNode
                currentDepth += 1
        return graph

    def drawDiagram(self, graph, file_path):
        with open(file_path, 'w') as file:
            file.write("graph ChessTree {\n")
            file.write('\trankdir="LR";\n')
            for node in graph.nodes:
                if node.ply_count % 2 == 1:
                    file.write(
                        f"\t{node.nodeID} [label = \"{node.name}\n{node.meta['white_wins']}, {node.meta['draws']}, {node.meta['black_wins']}\"]; \n")
                else:
                    file.write(
                        f"\t{node.nodeID} [label = \"{node.name}\n{node.meta['white_wins']}, {node.meta['draws']}, {node.meta['black_wins']}\", style = filled, fillcolor = black, fontcolor = white]; \n")
            for edge in graph.edges:
                file.write(
                    f"\t{edge.getSourceNode().nodeID} -- {edge.getTargetNode().nodeID};\n")
            file.write("}")

    def drawPopularOpenings(self, graph, file_path, depth, treshhold):
        with open(file_path, 'w') as file:
            file.write("graph ChessOpenings {\n")
            file.write('\trankdir="LR";\n')
            for node in graph.nodes:
                if (node.getGamesPlayed() > treshhold) and (node.getMoveNumber() <= depth):
                    if node.ply_count % 2 == 1:
                        file.write(
                            f"\t{node.nodeID} [label = \"{node.name}\n{node.meta['white_wins']}, {node.meta['draws']}, {node.meta['black_wins']}\"]; \n")
                    else:
                        file.write(
                            f"\t{node.nodeID} [label = \"{node.name}\n{node.meta['white_wins']}, {node.meta['draws']}, {node.meta['black_wins']}\", style = filled, fillcolor = black, fontcolor = white]; \n")
            for edge in graph.edges:
                if (edge.getTargetNode().getGamesPlayed() > treshhold) and (edge.getTargetNode().getMoveNumber() <= depth):
                    file.write(
                        f"\t{edge.getSourceNode().nodeID} -- {edge.getTargetNode().nodeID};\n")
            file.write("}")


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
                sourceNode = graph.lookForNodeInChildren(sourceNodeName)
                targetNode = graph.lookForNodeInChildren(targetNodeName)
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


# lookForNodeInChildren(move, moveCount, previousMoves[])
# createNewNode(move, moveCount, previousMoves[]). Oppretter en edge fra siste node i previousMoves til denne.
# addNode
# if lookForNodeInChildren
#increaseWeight(node, node.previousMoves[-1])
