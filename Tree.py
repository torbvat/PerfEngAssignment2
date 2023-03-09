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

    def setRootName(self, name):
        self.root.name = name

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
    def __init__(self):
        pass

    def lookForNodeInChildren(self, move_name, children):
        for node in children:
            if node.getName() == move_name:
                return node
        return None

    # Creates a graph of the first 'max_steps' moves of each game given in the constructor
    def createGraph(self, games, max_steps=500): 
        if max_steps < 1:
            raise ValueError("Max steps must be greater than 0")
        graph = Graph(games)
        for game in games:
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
    """
    # Writes the entire graph to a file in the DOT language
    def drawGraph(self, graph, file_path):
        with open(file_path, 'w') as file:
            file.write("graph ChessTree {\n")
            file.write('\trankdir="LR";\n')
            for node in graph.getNodes():
                if node.isWhitePlayer():
                    file.write(
                        f"\t{node.getID()} [label = \"{node.getName()}\n{node.getResultCounts()['white_wins']}, {node.getResultCounts()['draws']}, {node.getResultCounts()['black_wins']}\"]; \n")
                else:
                    file.write(
                        f"\t{node.getID()} [label = \"{node.getName()}\n{node.getResultCounts()['white_wins']}, {node.getResultCounts()['draws']}, {node.getResultCounts()['black_wins']}\"; style = filled, fillcolor = black, fontcolor = white]; \n")
            for edge in graph.getEdges():
                file.write(
                    f"\t{edge.getSourceNode().getID()} -- {edge.getTargetNode().getID()};\n")
            file.write("}")
    """

    # Writes the graph to a file in the DOT language, but only writes nodes that have been played more than 'threshold' times,
    # and only 'depth' moves deep
    def drawGraph(self, graph, file_path, depth=10, threshold=1):
        if threshold < 1 or depth < 1:
            raise ValueError("Threshold and depth must be greater than 0")
        with open(file_path, 'w') as file:
            file.write("graph ChessOpenings {\n")
            file.write('\trankdir="LR";\n')
            root = graph.getRoot()

            # Adds up the result counts of all the children of the root node 
            for i in range(0, len(graph.getRoot().getChildren())):
                graph.getRoot().getResultCounts()["white_wins"] += graph.getRoot().getChildren()[i].getResultCounts()['white_wins']
                graph.getRoot().getResultCounts()["black_wins"] += graph.getRoot().getChildren()[i].getResultCounts()['black_wins']
                graph.getRoot().getResultCounts()["draws"] += graph.getRoot().getChildren()[i].getResultCounts()['draws']
           
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
            file.write(f"\t{root.getID()} [label = \"{root.getName()}\n{root.getResultCounts()['white_wins']}, {root.getResultCounts()['draws']}, {root.getResultCounts()['black_wins']}\", shape = octagon, style = filled, fillcolor = green, fontcolor = white]; \n")
            file.write("}")

    # Writes a graph of the games with a certain opening to a DOT-file
    def drawGamesWithOpening(self, file_path, opening, games, depth=500, threshold=1):
        if depth < 1 or threshold < 1:
            raise ValueError("Depth and threshold must be greater than 0")
        relevant_games = []
        for game in games:
            if game.getOpening() == opening:
                relevant_games.append(game)
        graph = self.createGraph(relevant_games, depth)
        graph.setRootName(opening)
        self.drawGraph(graph, file_path, depth, threshold)
