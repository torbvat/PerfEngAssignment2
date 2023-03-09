# Graphs
import DatabaseHandler
# Nodes
# --------


class Node:
    def __init__(self, move, ply_count=0, node_ID=0):
        self.name = move.getMoveText() if not ply_count == 0 else "Root"
        self.result_counts = {
            'white_wins': 0,
            'black_wins': 0,
            'draws': 0,
        }
        self.children = []
        self.ply_count = ply_count
        self.white_player = True if int(self.ply_count) % 2 == 1 else False
        self.node_ID = node_ID

    def getName(self):
        return self.name
    
    def getPlyCount(self):
        return self.ply_count
    
    def getID(self):
        return self.node_ID
    
    def getResultCounts(self):
        return self.result_counts

    def getGamesPlayed(self):
        return sum(self.result_counts.values())

    def getChildren(self):
        return self.children
    
    def isWhitePlayer(self):
        return self.white_player

    def __repr__(self):
        return (f"|{self.name} : {self.ply_count} : {len(self.children)}|")
# Edges
# --------


class Edge:
    def __init__(self, source_node, target_node):
        self.source_node = source_node
        self.target_node = target_node

    def getSourceNode(self):
        return self.source_node

    def getTargetNode(self):
        return self.target_node

# Graphs
# ---------


class Graph:
    def __init__(self, games):
        self.edges = []
        self.games = games
        self.root = Node("", 0, 0)
        self.nodes = [self.root]
        self.node_ID = 1

    def getID(self):
        return self.node_ID

    def increaseID(self):
        self.node_ID += 1

    def getNodes(self):
        return self.nodes
    
    def getEdges(self):
        return self.edges
    
    def getRoot(self):
        return self.root

    def getGames(self):
        return self.games

    def lookForEdge(self, source_node, target_node):
        for edge in self.getEdges():
            if edge.getSourceNode() == source_node and edge.getTargetNode() == target_node:
                return edge
        return None

    def newNode(self, move, ply_count, current_node, winner):
        new_node = Node(move, ply_count, self.getID())
        new_node.result_counts[winner] += 1
        self.nodes.append(new_node)
        self.edges.append(Edge(current_node, new_node))
        self.increaseID()
        return new_node

# Printer
# ----------


class Printer:
    def __init__(self, games):
        self.games = games

    def lookForNodeInChildren(self, move_name, children):
        for node in children:
            if node.getName() == move_name:
                return node
        return None

    # Creates a graph of the first 'max_steps' moves of each game given in the constructor
    def createGraph(self, max_steps=500): 
        if max_steps < 1:
            raise ValueError("Max steps must be greater than 0")
        graph = Graph(self.games)
        for game in self.games:
            if game.getResult() == "1-0":
                winner = "white_wins"
            elif game.getResult() == "0-1":
                winner = "black_wins"
            else:
                winner = "draws"

            current_node = graph.getRoot()
            current_depth = 0
            #Iterate through the moves of the game until the max depth is reached or the end of the game is reached
            for move in game.getMoves()[:max_steps] if max_steps < len(game.getMoves()) else game.getMoves():
                next_node = self.lookForNodeInChildren(move.getMoveText(), current_node.getChildren())
                if next_node: #If the node already exists, just increment the result count and move on
                    next_node.getResultCounts()[winner] += 1
                    current_node = next_node 
                    current_depth += 1
                else:
                    break #If the node doesn't exist, break out of the loop and create the rest of the nodes (loop below)
            for move in game.getMoves()[current_depth:max_steps] if max_steps < len(game.getMoves()) else game.getMoves()[current_depth:]:  
                new_node = graph.newNode(move, current_depth+1, current_node, winner) 
                current_node.children.append(new_node)
                current_node = new_node
                current_depth += 1
        return graph

    # Writes the entire graph to a file in the DOT language
    def drawGraph(self, graph, file_path):
        with open(file_path, 'w') as file:
            file.write("graph ChessTree {\n")
            for node in graph.getNodes():
                if node.isWhitePlayer():
                    file.write(
                        f"\t{node.getID()} [label = \"{node.getName()}\"]; \n")
                else:
                    file.write(
                        f"\t{node.getID()} [label = \"{node.getName()}\", style = filled, fillcolor = black, fontcolor = white]; \n")
            for edge in graph.getEdges():
                file.write(
                    f"\t{edge.getSourceNode().getID()} -- {edge.getTargetNode().getID()};\n")
            file.write("}")

    # Writes the graph to a file in the DOT language, but only writes nodes that have been played more than 'threshold' times,
    # and only 'depth' moves deep
    def drawPopularOpenings(self, graph, file_path, depth=5, threshold=1):
        if threshold < 1 or depth < 1:
            raise ValueError("Threshold and depth must be greater than 0")
        with open(file_path, 'w') as file:
            file.write("graph ChessOpenings {\n")
            for node in graph.getNodes():
                if (node.getGamesPlayed() > threshold) and (node.getPlyCount() <= depth):
                    if node.isWhitePlayer():
                        file.write(
                            f"\t{node.getID()} [label = \"{node.getName()}\n{node.getResultCounts()['white_wins']}, {node.getResultCounts()['draws']}, {node.getResultCounts()['black_wins']}\"]; \n")
                    else:
                        file.write(
                            f"\t{node.getID()} [label = \"{node.getName()}\n{node.getResultCounts()['white_wins']}, {node.getResultCounts()['draws']}, {node.getResultCounts()['black_wins']}\", style = filled, fillcolor = black, fontcolor = white]; \n")
            for edge in graph.getEdges():
                if (edge.getTargetNode().getGamesPlayed() > threshold) and (edge.getTargetNode().getPlyCount() <= depth):
                    file.write(
                        f"\t{edge.getSourceNode().getID()} -- {edge.getTargetNode().getID()};\n")
            file.write("}")

    #UNFINISHED
    def drawOpening(self, graph, file_path, opening, depth):
        if depth < 1:
            raise ValueError("Depth must be greater than 0")
        with open(file_path, 'w') as file:
            file.write("graph OpeningTree {\n")
            for game in graph.getGames():
                if game.getOpening() == opening:
                    for node in graph.getNodes():
                        if node.getName() == opening and node.getMoveNumber() <= depth:
                            if node.isWhitePlayer():
                                file.write(
                                    f"\t{node.getID()} [label = \"{node.getName()}\"]; \n")
                            else:
                                file.write(
                                    f"\t{node.getID()} [label = \"{node.getName()}\", style = filled, fillcolor = black, fontcolor = white]; \n")
                    for edge in graph.getEdges():
                        if edge.getSourceNode().getName() == opening and edge.getTargetNode().getMoveNumber() <= depth:
                            file.write(
                                f"\t{edge.getSourceNode().getID()} -- {edge.getTargetNode().getID()};\n")
            file.write("}")