class Player:
    def __init__(self, name, startingRoom):
        self.name = name
        self.currentRoom = startingRoom
    def travel(self, direction, showRooms = False):
        nextRoom = self.currentRoom.getRoomInDirection(direction)
        if nextRoom is not None:
            self.currentRoom = nextRoom
            if (showRooms):
                nextRoom.printRoomDescription(self)
        else:
            print("You cannot move in that direction.")
    
    def traverse(self, totalRooms):      
        opposites = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
        unexploredPaths = 0
        path=[]
        visited=set()
        graph={}

        while True:
            exits = self.currentRoom.getExits()

            if self.currentRoom.id not in graph:
                graph[self.currentRoom.id] = {}
                for dir in exits:
                    graph[self.currentRoom.id][dir] = "?"
                    unexploredPaths += 1

            visited.add(self.currentRoom.id)

            unexploredExits = [dir for dir in exits if graph[self.currentRoom.id][dir] is "?"]
            if not len(unexploredExits):
                if len(path) is 1:
                    return graph
                wayBack = opposites[path.pop()]
                self.travel(wayBack)
            else:
                wayForward = unexploredExits[0]
                graph[self.currentRoom.id][wayForward] = self.currentRoom.getRoomInDirection(wayForward).id
                unexploredPaths -= 1
                self.travel(wayForward)
                path.append(wayForward)

            if len(visited) >= totalRooms and not unexploredPaths:
                return graph
