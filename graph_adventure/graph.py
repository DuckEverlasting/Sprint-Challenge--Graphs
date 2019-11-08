import random
from util import Queue


class Graph:
    def __init__(self, data):
        self.graph = data
        self.size = len(data)
        self.savedPaths = {}

    def getExits(self, room, exclude=-1):
        return [self.graph[room][i] for i in self.graph[room] if self.graph[room][i] != exclude]

    def bfs(self, start, finish):
        queue = Queue()
        queue.enqueue([start])
        visited = set()
        bestPath = None
        bestLength = 0
        while queue.size:
            current = queue.dequeue()
            currentRoom = current[-1]
            visited.add(currentRoom)
            if currentRoom == finish:
                if not bestLength or len(current) < bestLength:
                    bestPath = current
                    bestLength = len(bestPath)
            else:
                for dir in self.graph[currentRoom]:
                    dest = self.graph[currentRoom][dir]
                    if dest not in visited:
                        queue.enqueue(current + [dest])

        if bestLength:
            bestPath.pop(0)
            return bestPath
        return None


    def pathfind(self, graph, start, previous):
        if start in self.savedPaths and previous in self.savedPaths[start]:
            return self.savedPaths[start][previous]

        if len(graph) == 1:
            return [start]

        current = start
        path = [start]
        visited = set([start])

        while len(visited) < len(graph):
            exits = self.getExits(current)
            unvisited = [i for i in exits if i is not previous and i not in visited]
            if len(unvisited) == 0:
                pathBack = self.bfs(current, start)
                path.extend(pathBack)
                if start not in self.savedPaths:
                    self.savedPaths[start] = {}
                self.savedPaths[start][previous] = path
                return path
            elif len(unvisited) == 1:
                previous = current
                current = unvisited[0]
                path.append(current)
            else:
                bestLength = self.size
                bestPath = None
                for exit in unvisited:
                    subgraph = self.attemptSubGraph(exit, current)
                    if subgraph and len(subgraph) < bestLength:
                        subpath = self.pathfind(subgraph, exit, current)
                        if subpath:
                            bestLength = len(subgraph)
                            bestPath = subpath
                if not bestPath:
                    return None
                path.extend(bestPath + [current])
                for i in bestPath:
                    visited.add(i)

    def attemptSubGraph(self, start, previousRoom, maxSize=200):
        opposites = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
        unexploredPaths = 0
        path=[]
        subgraph = {}
        exits = [i for i in self.graph[start] if self.graph[start][i] != previousRoom]
        subgraph[start] = {}
        current = start

        if not len(exits):
            return {start: {}}

        for dir in exits:
            subgraph[start][dir] = "?"
            unexploredPaths += 1
                
        while True:
            exits = [i for i in self.graph[current]]

            if current not in subgraph:
                subgraph[current] = {}
                for dir in exits:
                    subgraph[current][dir] = "?"
                    unexploredPaths += 1

            unexploredExits = []
            for dir in exits:
                if self.graph[current][dir] != previousRoom:
                    if subgraph[current][dir] is "?":
                        unexploredExits.append(dir)
                elif current != start:
                    return None

            if not len(unexploredExits):
                if len(path) is 1:
                    return subgraph
                wayBack = opposites[path.pop()]
                current = subgraph[current][wayBack]
            else:
                wayForward = unexploredExits[0]
                subgraph[current][wayForward] = self.graph[current][wayForward]
                unexploredPaths -= 1
                current = subgraph[current][wayForward]
                path.append(wayForward)

            if len(subgraph) > maxSize:
                return None


    def findNearestUnexplored(self, start, targets):
        output = []
        queue = Queue()
        localExplored = set()
        queue.enqueue(start)
        while queue.size:
            current = queue.dequeue()
            for i in self.graph[current]:
                room = self.graph[current][i]
                if room not in localExplored:
                    if room in targets:
                        output.append(room)
                    queue.enqueue(room)
            if len(output):
                return [output, current]
            localExplored.add(current)


    def smartTraverse(self, start=0, targetLength=1000):
        traversalPath = []
        current = start
        targets = set([i for i in range(1, self.size)])

        while len(targets):
            nearestUnexplored, connecting = self.findNearestUnexplored(current, targets)
            bestLength = self.size
            bestPath = None
            for exit in nearestUnexplored:
                subgraph = self.attemptSubGraph(exit, connecting)
                if subgraph and len(subgraph) < bestLength:
                    subpath = self.pathfind(subgraph, exit, current)
                    if subpath:
                        bestLength = len(subgraph)
                        bestPath = subpath
            if not bestPath:
                next = random.choice(nearestUnexplored)
                addition = self.bfs(current, next)
                for i in addition:
                    traversalPath.append(i)
                    if i in targets:
                        targets.remove(i)
                current = next
            else:
                addition = bestPath + [current]
                for i in addition:
                    traversalPath.append(i)
                    if i in targets:
                        targets.remove(i)
                    if not len(targets):
                        return traversalPath
            
            if len(traversalPath) > targetLength:
                return None
        return traversalPath
    
    def convertPathToDirections(self, path, start=0):
        current = start
        next = path[0]
        index = 0
        directions = []
        while True:
            error = True
            for dir in self.graph[current]:
                if self.graph[current][dir] == next:
                    directions.append(dir)
                    error = False
                    break
            if error:
                print("ERROR - INDEX:", index, "ROOM:", current)
            current = next
            index += 1
            try:
                next = path[index]
            except:
                break
        return directions