import random
from util import Queue


class Graph:
    def __init__(self, data):
        self.graph = data
        self.size = len(data)
        self.savedPaths = {}

    def superBfs(self, start, finish):
        queue = Queue()
        queue.enqueue([[None], [start]])
        visited = set()
        bestPath = None
        bestLength = 0
        while queue.size:
            current = queue.dequeue()
            currentRoom = current[1][-1]
            visited.add(currentRoom)
            if currentRoom == finish:
                if not bestLength or len(current[0]) < bestLength:
                    bestPath = [current[0], current[1]]
                    bestLength = len(bestPath[0])
            else:
                for dir in self.graph[currentRoom]:
                    dest = self.graph[currentRoom][dir]
                    if dest not in visited:
                        queue.enqueue([current[0] + [dir], current[1] + [dest]])

        if bestLength:
            bestPath[0].pop(0)
            bestPath[1].pop(0)
            return bestPath
        return None

    def subgraphBestTraversal(self, graph, start=0):
        queue = Queue()
        queue.enqueue([[None], [start], {}])
        bestPath = []
        bestLength = None
        previousRoom = None
        currentRoom = None
        while queue.size:
            previousRoom = currentRoom
            current = queue.dequeue()
            currentRoom = current[1][-1]
            currentGraph = current[2]

            if currentRoom not in currentGraph:
                currentGraph[currentRoom] = ""

            if currentRoom in self.savedPaths:
                if previousRoom in self.savedPaths[currentRoom]:
                    shortcut = self.savedPaths[currentRoom][previousRoom]
                    current[0].extend(shortcut[0])
                    current[1].extend(shortcut[1])
                    for dir in self.graph[currentRoom]:
                        if self.graph[currentRoom][dir] != previousRoom:
                            currentGraph[currentRoom] += dir

            if len(currentGraph) == len(graph) and currentRoom == start:
                if not bestLength or len(current[0]) < bestLength:
                    bestPath = [current[0], current[1]]
                    bestLength = len(bestPath[0])
            elif not bestLength or len(current[0]) < bestLength:
                for dir in graph[currentRoom]:
                    dest = graph[currentRoom][dir]
                    if dir not in currentGraph[currentRoom]:
                        graphCopy = currentGraph.copy()
                        graphCopy[currentRoom] += dir
                        queue.enqueue([current[0] + [dir], current[1] + [dest], graphCopy])

        if len(bestPath):
            bestPath[0].pop(0)
            bestPath[1].pop(0)
        return bestPath

    def attemptSubGraph(self, start, previousRoom, maxSize=50, retSize=False):
        opposites = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
        unexploredPaths = 0
        path=[]
        subgraph = {}
        exits = [dir for dir in self.graph[start]]
        subgraph[start] = {}
        current = start
        for dir in exits:
            if self.graph[start][dir] != previousRoom:
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
                    return 0

            if not len(unexploredExits):
                if len(path) is 1:
                    if retSize:
                        return len(subgraph)
                    else:
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
                return 0


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

    def getTraversalPath(self, lockedTargetOrder=[0]):
        traversalPath = []
        targetOrder = lockedTargetOrder[:]
        previousTarget = None
        currentTarget = targetOrder.pop(0)

        targetList = [i for i in range(1, self.size)]
        targets = set()
        for i in targetList:
            targets.add(i)
        while len(targets):
            previousTarget = currentTarget
            if len(targetOrder):
                currentTarget = targetOrder.pop(0)
            else:
                currentTarget = random.choice(self.findNearestUnexplored(currentTarget, targets))
            targets.remove(currentTarget)
            currentPath = self.superBfs(previousTarget, currentTarget)
            if not currentPath:
                print("ERROR")
                break
            for room in currentPath[1]:
                if room in targets:
                    targets.remove(int(room))
            for dir in currentPath[0]:
                traversalPath.append(dir)
        return traversalPath

    def getAllSubpathData(self, subpathSize):
        subpathGraph = {}
        targetList = [i for i in range(1, self.size)]
        targets = set()
        for i in targetList:
            targets.add(i)
        
        for room in self.graph:
            if int(room) in targets and len(self.graph[room]) == 2:
                for dir in self.graph[room]:
                    connecting = self.graph[room][dir]
                    subgraph = self.attemptSubGraph(room, connecting, subpathSize)
                    if subgraph:
                        if room not in subpathGraph:
                            subpathGraph[room] = {}
                        bestTrav = self.subgraphBestTraversal(subgraph, room)
                        if len(bestTrav):
                            for i in bestTrav[1]:
                                if i in targets:
                                    targets.remove(i)
                            subpathGraph[room][connecting] = bestTrav

        self.savedPaths = subpathGraph

    def smartTraverse(self, lockedTargetOrder=[0]):
        traversalPath = []
        targetOrder = lockedTargetOrder[:]
        previousTarget = None
        currentTarget = targetOrder.pop(0)

        targetList = [i for i in range(1, self.size)]
        targets = set()
        for i in targetList:
            targets.add(i)
        while len(targets):
            previousTarget = currentTarget
            if len(targetOrder):
                currentTarget = targetOrder.pop(0)
            else:
                nearestUnexplored, connecting = self.findNearestUnexplored(currentTarget, targets)
                if len(nearestUnexplored) > 1:
                    smallest = random.choice(nearestUnexplored)
                    if len(self.graph[smallest]) == 2:
                        smallestSize = self.attemptSubGraph(smallest, currentTarget, 100, retSize=True)
                    else:
                        smallestSize = None
                    for path in [i for i in nearestUnexplored if i != smallest]:
                        if len(self.graph[path]) == 2:
                            pathSize = self.attemptSubGraph(path, currentTarget, 100, retSize=True)
                            if pathSize:
                                if not smallestSize or smallestSize > pathSize:
                                    smallest = path
                    currentTarget = smallest
                else:
                    currentTarget = nearestUnexplored[0]
            targets.remove(currentTarget)
            currentPath = self.superBfs(previousTarget, currentTarget)
            if not currentPath:
                print("ERROR")
                break
            for room in currentPath[1]:
                if room in targets:
                    targets.remove(int(room))
            traversalPath.extend(currentPath[0])

            if currentTarget in self.savedPaths:
                if connecting in self.savedPaths[currentTarget]:
                    shortcut = self.savedPaths[currentTarget][connecting]
                    for room in shortcut[1]:
                        if room in targets:
                            targets.remove(int(room))
                    traversalPath.extend(shortcut[0])
            
            if len(traversalPath) > 1000:
                return None
        traversalPath.pop(0)                    
        return traversalPath
    
    def convertPathToDirections(self, path):
        pass