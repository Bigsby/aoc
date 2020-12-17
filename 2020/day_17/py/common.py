import sys, os

class Dimension(list):
    def __init__(self, upperLayer = None, outerDimension = False):
        self.offset = 0
        self.upperLayer = upperLayer
        if self.upperLayer is not None:
            self.upperLayer.append(self)
        self.outerDimension = outerDimension

    def __getitem__(self, key):
        return list.__getitem__(self, key + self.offset)
    def __setitem__(self, key, item):
        list.__setitem__(self, key + self.offset, item)
    def append(self, item):
        super().append(item)
        self.offset = len(self) // 2


    def _indexedlayers(self):
        return [ (index, layer) for index, layer in enumerate(self) ]

    def __str__(self):
        if len(self):
            if self.outerDimension:
                return "".join(map(lambda indexedLayer: "".join(f"z={indexedLayer[0] - self.offset}\n{indexedLayer[1]}\n"), self._indexedlayers()))
            elif len(self) and isinstance(self[0], self.__class__):
                return "\n".join(map(lambda subLayer: str(subLayer), self))
            else:
                return "".join(map(lambda item: "#" if item else ".", self))
        else:
            return list.__str__(self)


class Cube(Dimension):
    def __init__(self):
        super().__init__(None, True)

    def isPositionValid(self, position):
        currentDimension = self
        for coordinate in position:
            if coordinate < -currentDimension.offset or coordinate > currentDimension.offset:
                return False
            if len(currentDimension) == 0:
                return False
            currentDimension = currentDimension[0]
        return True

    def getNeighbors(self, position):
        positionZ, positionX, positionY = position
        for z in range(positionZ - 1, positionZ + 2):
            for x in range(positionX - 1, positionX + 2):
                for y in range(positionY - 1, positionY + 2):
                    neighbor = (z, x, y)
                    if neighbor != position:
                        yield neighbor
                    

    def getLimits(self):
        limits = [ ]
        currentDimension = self
        while isinstance(currentDimension, Dimension):
            limits.append(currentDimension.offset)
            if len(currentDimension) == 0:
                break
            currentDimension = currentDimension[0]
        return tuple(limits)

    def isPositionActive(self, position):
        try:
            return self.isPositionValid(position) and self[position[0]][position[1]][position[2]]
        except:
            return False


    def getActiveCountForNeighbors(self, neighbors):
        return sum(map(lambda neighbor: self.isPositionActive(neighbor), neighbors))



    def getNextStep(self):
        newState = Cube()
        zLimit, xLimit, yLimit = self.getLimits()
        newPositions = []

        for z in range(-zLimit - 1, zLimit + 2):
            layer = Dimension(newState)
            for x in range(-xLimit -1, xLimit + 2):
                row = Dimension(layer)
                for y in range(-yLimit -1, yLimit + 2):
                    position = (z, x, y)
                    neighbors = self.getNeighbors(position)
                    neighborsActiveCount = self.getActiveCountForNeighbors(neighbors)
                    newValue = False
                    if self.isPositionActive(position):
                        newValue = neighborsActiveCount == 2 or neighborsActiveCount == 3
                    else:
                        newValue = neighborsActiveCount == 3

                    newPositions.append((position, newValue))
                    row.append(newValue)
            

        return newState


    def getActiveCount(self):
        activeCount = 0
        zLimit, xLimit, yLimit = self.getLimits()
        for z in range(-zLimit, zLimit + 1):
            for x in range(-xLimit, xLimit + 1):
                for y in range(-yLimit, yLimit + 1):
                    activeCount += self[z][x][y]
        return activeCount



def getInput():
    if len(sys.argv) != 2:
        print("Please, add input file path as parameter")
        sys.exit(1)

    filePath = sys.argv[1]
    if not os.path.isfile(filePath):
        print("File not found")
        sys.exit(1)

    cube = Cube()
    layer = None
    with open(filePath, "r") as file:
        for line in file.readlines():
            if layer is None:
                layer = Dimension(cube)
            row = Dimension(layer)
            for c in line.strip():
                row.append(True if c == "#" else False)
    return cube
