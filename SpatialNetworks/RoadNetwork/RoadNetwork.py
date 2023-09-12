START_NODE = 1
END_NODE = 10

import heapq
import math


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


def heuristic(node1, node2):
    return math.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2)


def dijkstra(startId, endId, nodes):
    nodesVisited = 0

    # initialize distances
    distances = {node.id: float("inf") for node in nodes.values()}

    # set start node distance to 0
    distances[startId] = 0

    # initialize a priority queue with start node
    pq = [(0, startId)]

    # while priority queue is not empty
    while pq:
        # get the top node from the priority queue (min distance)
        currentDist, currentNodeId = heapq.heappop(pq)
        nodesVisited += 1

        # if the top node is the end node, break
        # shortest path is found
        if currentNodeId == endId:
            break

        # if the top node distance is greater than the
        # distance in the distances dictionary, skip
        if currentDist > distances[currentNodeId]:
            continue

        # for each neighbour of the top node
        currentNode = nodes[currentNodeId]
        for neighbourId, neighbourDist in currentNode.neighbours.items():
            # calculate the new distance as the sum of the current distance
            # and the distance to the neighbour
            newDist = currentDist + neighbourDist

            # if the new distance is less than the distance in the
            # distances dictionary update the distance and push the
            # neighbour to the priority queue
            if newDist < distances[neighbourId]:
                distances[neighbourId] = newDist
                heapq.heappush(pq, (newDist, neighbourId))

    # reconstruct the path
    path = []

    # start from the end node
    currentNode = nodes[endId]

    while currentNodeId is not None:
        # add the current node to the path
        path.append(currentNode.id)

        # if the current node is the start node, break
        if currentNode.id == startId:
            break

        # get the neighbors of the current node
        neighbors = [
            (neighbourId, distances[neighbourId])
            for neighbourId in currentNode.neighbours
        ]

        # if there are no neighbors, break (prevent inf looping)
        if not neighbors:
            break

        # get the neighbor with the minimum distance
        minNeighbor = min(neighbors, key=lambda x: x[1])
        currentNode = nodes[minNeighbor[0]]

    # reverse the path from start to end
    path.reverse()

    # nodes visited -1 because the end node is also visited
    return path, distances[endId], nodesVisited - 1


def aStar(startId, endId, nodes):
    nodesVisited = 0

    # initialize distances
    distances = {node.id: float("inf") for node in nodes.values()}

    # set start node distance to 0
    distances[startId] = 0

    # initialize a priority queue with start node
    pq = [(0, startId)]

    # while priority queue is not empty
    while pq:
        currentDist, currentNodeId = heapq.heappop(pq)
        nodesVisited += 1

        # if the top node is the end node, break
        # shortest path is found
        if currentNodeId == endId:
            print("found")
            break

        # if the top node distance is greater than the
        # distance in the distances dictionary, skip
        if currentDist > distances[currentNodeId]:
            continue

        # for each neighbour of the top node
        currentNode = nodes[currentNodeId]
        for neighbourId, neighbourDist in currentNode.neighbours.items():
            # calculate the new distance as the sum of the current distance
            # and the distance to the neighbour
            newDist = (
                currentDist
                + neighbourDist
                + heuristic(nodes[neighbourId], nodes[endId])
            )

            # if the new distance is less than the distance in the
            # distances dictionary update the distance using the
            # heuristic function and push the neighbour to the priority queue
            if newDist < distances[neighbourId]:
                distances[neighbourId] = newDist
                heapq.heappush(pq, (newDist, neighbourId))

    # reconstruct the path
    path = []

    # start from the end node
    currentNode = nodes[endId]

    while currentNodeId is not None:
        # add the current node to the path
        path.append(currentNode.id)

        # if the current node is the start node, break
        if currentNode.id == startId:
            break

        # get the neighbors of the current node
        neighbors = [
            (neighbourId, distances[neighbourId])
            for neighbourId in currentNode.neighbours
        ]

        # if there are no neighbors, break (prevent inf looping)
        if not neighbors:
            break

        # get the neighbor with the minimum distance
        minNeighbor = min(neighbors, key=lambda x: x[1])
        currentNode = nodes[minNeighbor[0]]

    # reverse the path from start to end
    path.reverse()

    # nodes visited -1 because the end node is also visited
    return path, distances[endId], nodesVisited - 1


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

    # write network to file
    with open("../data/outputs/out.txt", "w") as fo:
        for node in nodes.values():
            node.writeToFile(fo)

    with open("../data/outputs/path.txt", "w") as fp:
        pathDijkstra, distanceDijkstra, nodesVisitedDijkstra = dijkstra(
            START_NODE, END_NODE, nodes
        )

        fp.write(
            f"Dijkstra:\n-Shortest path length: {len(pathDijkstra)}\n-Shortest path distance: {distanceDijkstra}\n-Shortest path: {pathDijkstra}\n-Nodes visited: {nodesVisitedDijkstra}\n\n"
        )

        pathAStar, distanceAStar, nodesVisitedAStar = aStar(START_NODE, END_NODE, nodes)

        fp.write(
            f"Astar (A*):\n-Shortest path length: {len(pathAStar)}\n-Shortest path distance: {distanceAStar}\n-Shortest path: {pathAStar}\n-Nodes visited: {nodesVisitedAStar}\n"
        )


if __name__ == "__main__":
    main()
