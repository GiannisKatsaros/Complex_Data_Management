class Polygon:
    def __init__(self, coords, id):
        self.coords = coords
        self.id = id
        self.calculateMBR()
        self.calculateCenter()
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

    def calculateCenter(self):
        self.centerX = sum([x[0] for x in self.coords]) / len(self.coords)
        self.centerY = sum([x[1] for x in self.coords]) / len(self.coords)

    def calculateZorder(self):
        int_X = int((self.centerX - self.minX) * 1e6)
        int_Y = int((self.centerY - self.minY) * 1e6)
        self.zorder = 0
        for i in range(32):
            self.zorder |= (int_X & (1 << i)) << i | (int_Y & (1 << i)) << (i + 1)


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
                for polygon in polygons:
                    fr.write(str(polygon.id) + "," + str(polygon.zorder) + "\n")


if __name__ == "__main__":
    main()
