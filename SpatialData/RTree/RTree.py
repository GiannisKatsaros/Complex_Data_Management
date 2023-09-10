MAX_ENTRIES = 20
MIN_ENTRIES = 8


# calculate minimum bounding rectangle
def calculateMBR(coordinates):
    minX = coordinates[0][0]
    maxX = coordinates[0][0]
    minY = coordinates[0][1]
    maxY = coordinates[0][1]
    for coordinate in coordinates:
        if coordinate[0] < minX:
            minX = coordinate[0]
        elif coordinate[0] > maxX:
            maxX = coordinate[0]
        if coordinate[1] < minY:
            minY = coordinate[1]
        elif coordinate[1] > maxY:
            maxY = coordinate[1]
    mbr = [[minX, minY], [minX, maxY], [maxX, minY], [maxX, maxY]]
    return mbr


class RTreeNode:
    def __init__(self, children=None, isLeaf=True, id=None):
        self.children = children or []
        self.isLeaf = isLeaf
        self.id = id

        self.calculateNodeMBR()

        # calculate only if node is a leaf
        if isLeaf:
            self.calculateCenter()
            self.calculateZorder()

    # calculate minimum bounding rectangle
    def calculateNodeMBR(self):
        if self.isLeaf:
            self.MBR = calculateMBR(self.children)
        else:
            self.MBR = calculateMBR(
                [coord for child in self.children for coord in child.MBR]
            )

    # calculate center of MBR
    def calculateCenter(self):
        self.centerX = self.MBR[0][0] + (self.MBR[2][0] - self.MBR[0][0]) / 2
        self.centerY = self.MBR[0][1] + (self.MBR[1][1] - self.MBR[0][1]) / 2

    # calculate z-order
    def calculateZorder(self):
        int_X = int((self.centerX - self.MBR[0][0]) * 1e6)
        int_Y = int((self.centerY - self.MBR[0][1]) * 1e6)
        self.zorder = 0
        for i in range(32):
            self.zorder |= (int_X & (1 << i)) << i | (int_Y & (1 << i)) << (i + 1)


class RTree:
    def __init__(self, startingId=0, maxChildren=MAX_ENTRIES, minChildren=MIN_ENTRIES):
        self.startingId = startingId
        self.maxChildren = maxChildren
        self.minChildren = minChildren
        self.root = None

    def buildTree(self, nodes):
        if len(nodes) == 0:
            return None
        elif len(nodes) < 20:
            self.root = RTreeNode(nodes, False, self.startingId)
            return self.root
        else:
            splittedNodes = []
            if (
                len(nodes) % self.maxChildren > self.minChildren
                or len(nodes) % self.maxChildren == 0
            ):
                # split into nodes of maxChildren
                # and add the remaining to the last node
                for i in range(0, len(nodes), self.maxChildren):
                    splittedNodes.append(nodes[i : i + self.maxChildren])

            else:
                # split into two lists, one with minChildren
                # (remainingNodes)
                # and the other with the rest
                # (reducedNodes)
                reducedNodes = nodes[: len(nodes) - self.minChildren]
                remainingNodes = nodes[len(nodes) - self.minChildren :]

                # split into nodes of maxChildren
                # and add the remaining to the last node
                for i in range(0, len(reducedNodes), self.maxChildren):
                    splittedNodes.append(reducedNodes[i : i + self.maxChildren])

                # add the remaining polygons to the last node
                splittedNodes.append(remainingNodes)

            # create new nodes
            for i in range(len(splittedNodes)):
                splittedNodes[i] = RTreeNode(
                    splittedNodes[i], isLeaf=False, id=self.startingId
                )
                self.startingId += 1

            # call recursive function to build the tree
            return self.buildTree(splittedNodes)


def writeToFile(fr, node, level=0):
    if node is None:
        return

    indent = "|\t\t" * level
    id = "Id: " + str(node.id) + "\t" + ("" if len(str(node.id)) > 3 else "\t")
    type = "Type: " + ("Leaf" if node.isLeaf else "Node") + "\t"
    size = "" if node.isLeaf else "Size: " + str(len(node.children)) + "\t"
    mbr = (
        "MBR: ["
        + str(node.MBR[0][0])
        + ", "
        + str(node.MBR[2][0])
        + ", "
        + str(node.MBR[0][1])
        + ", "
        + str(node.MBR[1][1])
        + "]"
        + "\t"
    )

    fr.write(f"{indent}{id}{type}{size}MBR: {mbr}\n")

    if not node.isLeaf:
        for child in node.children:
            writeToFile(fr, child, level + 1)


def main():
    with open("../data/inputs/coords.txt") as fc:
        with open("../data/inputs/offsets.txt") as fo:
            with open("../data/outputs/rtree.txt", "w") as fr:
                coords = []
                offsets = []
                polygons = []

                nodes = []

                # read coords
                for line in fc:
                    xCoord, yCoord = line.strip("\n").split(",")
                    xCoord = float(xCoord)
                    yCoord = float(yCoord)
                    coords.append([xCoord, yCoord])
                # read offsets
                for line in fo:
                    id, start, end = line.strip("\n").split(",")
                    id = int(id)
                    start = int(start)
                    end = int(end)
                    offsets.append([id, start, end])

                for i in range(len(offsets)):
                    nodes.append(
                        RTreeNode(
                            coords[offsets[i][1] : offsets[i][2]], True, offsets[i][0]
                        )
                    )
                nodes.sort(key=lambda x: x.zorder)

                rTree = RTree(startingId=offsets[-1][0] + 1)
                rTree.buildTree(nodes)
                writeToFile(fr, rTree.root)


if __name__ == "__main__":
    main()
