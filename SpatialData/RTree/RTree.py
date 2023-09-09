MAX_ENTRIES = 19
MIN_ENTRIES = 8


class RTreeNode:
    def __init__(self, Mbr, children=None, isLeaf=True):
        self.Mbr = Mbr
        self.children = children or []
        self.isLeaf = isLeaf
        # self.id = id
        # self.parent = None


class RTree:
    def __init__(self, maxChildren=MAX_ENTRIES, minChildren=MIN_ENTRIES):
        self.maxChildren = maxChildren
        self.minChildren = minChildren
        self.root = None

    def calculateMBR(self, polygons):
        minX = polygons[0].minX
        maxX = polygons[0].maxX
        minY = polygons[0].minY
        maxY = polygons[0].maxY
        for polygon in polygons:
            if polygon.minX < minX:
                minX = polygon.minX
            elif polygon.maxX > maxX:
                maxX = polygon.maxX
            if polygon.minY < minY:
                minY = polygon.minY
            elif polygon.maxY > maxY:
                maxY = polygon.maxY
        return [minX, maxX, minY, maxY]

    def buildTree(self, polygons):
        print(len(polygons) % self.maxChildren)
        if len(polygons) == 0:
            return None
        elif len(polygons) < 20:
            return RTree(self.calculateMBR(polygons), polygons, True)
        else:
            splittedPolygons = []
            if len(polygons) % self.maxChildren > self.minChildren:
                # split into nodes of maxChildren
                # and add the remaining to the last node
                for i in range(0, len(polygons), self.maxChildren):
                    splittedPolygons.append(polygons[i : i + self.maxChildren])
            else:
                # split into two lists, one with minChildren
                # (remainingPolygons)
                # and the other with the rest
                # (reducedPolygons)
                reducedPolygons = polygons[: len(polygons) - self.minChildren]
                remainingPolygons = polygons[len(polygons) - self.minChildren :]

                # split into nodes of maxChildren
                # and add the remaining to the last node
                for i in range(0, len(reducedPolygons), self.maxChildren):
                    splittedPolygons.append(reducedPolygons[i : i + self.maxChildren])

                # add the remaining polygons to the last node
                splittedPolygons.append(remainingPolygons)

            nodes = []
            for pol in splittedPolygons:
                nodes.append(RTreeNode(self.calculateMBR(pol), pol, False))
            self.leaves = nodes.copy()
            # call recursive function to build the tree
            self.toPrint = nodes


class Polygon:
    def __init__(self, coords, id, withZorder=True):
        self.coords = coords
        self.id = id
        self.calculateMBR()
        self.calculateCenter()
        if withZorder:
            self.calculateZorder()

    def calculateMBR(self):
        self.minX = self.coords[0][0]
        self.minY = self.coords[0][1]
        self.maxX = self.coords[0][0]
        self.maxY = self.coords[0][1]
        for coordinate in self.coords:
            if coordinate[0] < self.minX:
                self.minX = coordinate[0]
            elif coordinate[0] > self.maxX:
                self.maxX = coordinate[0]
            if coordinate[1] < self.minY:
                self.minY = coordinate[1]
            elif coordinate[1] > self.maxY:
                self.maxY = coordinate[1]
        self.MBR = [self.minX, self.maxX, self.minY, self.maxY]

    def calculateCenter(self):
        self.centerX = sum([x[0] for x in self.coords]) / len(self.coords)
        self.centerY = sum([x[1] for x in self.coords]) / len(self.coords)

    def calculateZorder(self):
        int_X = int((self.centerX - self.minX) * 1e6)
        int_Y = int((self.centerY - self.minY) * 1e6)
        self.zorder = 0
        for i in range(32):
            self.zorder |= (int_X & (1 << i)) << i | (int_Y & (1 << i)) << (i + 1)


def printPolygons(fr, polygons):
    for polygon in polygons:
        fr.write(
            "id: "
            + str(polygon.id)
            + "\t\tz-order: "
            + str(polygon.zorder)
            + "\t\tMBR: "
            + str(polygon.MBR)
            + "\n"
        )


""" def printSplittedPolygons(fr, splittedPolygons):
    for splittedPolygon in splittedPolygons:
        fr.write("length: " + str(len(splittedPolygon)) + "\n")
        for polygon in splittedPolygon:
            fr.write("id: " + str(polygon.id) + "\t\tMBR: " + str(polygon.MBR) + "\n")
        fr.write("\n") """


def printSplittedPolygons(fr, nodes):
    for node in nodes:
        fr.write("MBR: " + str(node.Mbr) + "\t\t#: " + str(len(node.children)) + "\n")
        for polygon in node.children:
            fr.write("id: " + str(polygon.id) + "\t\tMBR: " + str(polygon.MBR) + "\n")
        fr.write("\n")


def main():
    with open("../data/inputs/coords.txt") as fc:
        with open("../data/inputs/offsets.txt") as fo:
            with open("../data/outputs/rtree.txt", "w") as fr:
                coords = []
                offsets = []
                polygons = []
                for line in fc:
                    xCoord, yCoord = line.strip("\n").split(",")
                    xCoord = float(xCoord)
                    yCoord = float(yCoord)
                    coords.append([xCoord, yCoord])

                for line in fo:
                    id, start, end = line.strip("\n").split(",")
                    id = int(id)
                    start = int(start)
                    end = int(end)
                    offsets.append([id, start, end])

                for i in range(len(offsets)):
                    polygons.append(
                        Polygon(
                            coords[offsets[i][1] : offsets[i][2]],
                            offsets[i][0],
                        )
                    )
                polygons.sort(key=lambda x: x.zorder)
                # printPolygons(fr, polygons)
                rTree = RTree()
                rTree.buildTree(polygons)
                printSplittedPolygons(fr, rTree.toPrint)


if __name__ == "__main__":
    main()
