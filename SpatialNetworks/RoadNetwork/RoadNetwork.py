class Node:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.neighbours = {}

    def writeToFile(self, fd):
        idd = "Id: " + str(self.id) + "\t"
        coords = "Coords: " + str(self.x) + ", " + str(self.y) + "\t"
        neighbours = "Neighbours: ["

        for id in self.neighbours.keys():
            neighbours += "(" + str(id) + "): " + str(self.neighbours[id]) + ", "

        neighbours = neighbours[:-2]
        neighbours += "]\n"

        fd.write(f"{idd}{coords}{neighbours}")


def main():
    nodes = {}

    # read nodes
    with open("../data/inputs/nodes.txt") as fn:
        for line in fn:
            id, xCoord, yCoord = line.strip("\n").split(" ")
            nodes[int(id)] = Node(int(id), float(xCoord), float(yCoord))

    # read edges
    with open("../data/inputs/edges.txt") as fe:
        for line in fe:
            id, startId, endId, distance = line.strip("\n").split(" ")
            nodes[int(startId)].neighbours[int(endId)] = float(distance)
            nodes[int(endId)].neighbours[int(startId)] = float(distance)

    with open("../data/outputs/out.txt", "w") as fo:
        for node in nodes.values():
            node.writeToFile(fo)


if __name__ == "__main__":
    main()
