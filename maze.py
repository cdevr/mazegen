#!/usr/bin/python
# routines for working with mazes
import sys
import random


class WrongCoords:
    pass


class Maze:

    def __init__(self, w=10, h=10):
        self.w = w
        self.h = h
        # create the array as specified in python's FAQ
        self.hwalls = [[0] * (self.w - 1) for _ in range(self.h)]
        self.vwalls = [[0] * (self.w) for _ in range(self.h - 1)]

    def neighbors(self, x, y):
        r = []
        if x > 0:
            r += [(x - 1, y)]
        if y > 0:
            r += [(x, y - 1)]
        if x < self.w - 1:
            r += [(x + 1, y)]
        if y < self.h - 1:
            r += [(x, y + 1)]
        return r

    def setWall(self, (x1, y1), (x2, y2), v):
        if abs(x2 - x1) == 1:
            if not y1 == y2:
                raise WrongCoords()
            x = min(x1, x2)
            if x < 0:
                raise WrongCoords()
            elif x > self.w - 2:
                raise WrongCoords()
            else:
                self.hwalls[y1][x] = v
                return
        if abs(y2 - y1) == 1:
            if not x1 == x2:
                raise WrongCoords()
            y = min(y1, y2)
            if y < 0:
                raise WrongCoords()
            elif y > self.h - 2:
                raise WrongCoords()
            else:
                self.vwalls[y][x1] = v
                return
        raise WrongCoords()

    def getWall(self, (x1, y1), (x2, y2)):
        if abs(x2 - x1) == 1:
            if not y1 == y2:
                raise WrongCoords()
            x = min(x1, x2)
            if x < 0:
                return 1
            elif x > self.w - 2:
                return 1
            else:
                return self.hwalls[y1][x]
        if abs(y2 - y1) == 1:
            if not x2 == x1:
                raise WrongCoords()
            y = min(y1, y2)
            if y < 0:
                return 1
            elif y > self.h - 2:
                return 1
            else:
                return self.vwalls[y][x1]
        raise WrongCoords()

    def printMaze(self, prfn=sys.stdout.write):
        y = -1
        prfn("+")
        for x in range(self.w):
            if self.getWall((x, y), (x, y + 1)) == 1:
                prfn("--")
            else:
                prfn("  ")
            prfn("+")
        prfn("\n")
        for y in range(self.h):
            prfn("|")
            for x in range(self.w):
                if self.getWall((x, y), (x + 1, y)) == 1:
                    prfn("  |")
                else:
                    prfn("   ")
            prfn("\n" + "+")
            if y <= self.h - 1:
                for x in range(self.w):
                    if self.getWall((x, y), (x, y + 1)) == 1:
                        prfn("--")
                    else:
                        prfn("  ")
                    prfn("+")
                prfn("\n")

    def genRandomMazeWalls(self):
        self.hwalls = [map(lambda _: random.choice((0, 1)), [0] * (self.w - 1))
                       for _ in range(self.h)]
        self.vwalls = [map(lambda _: random.choice((0, 1)), [0] * (self.w))
                       for _ in range(self.h - 1)]

    def setAllWalls(self, v):
        self.hwalls = [[v] * (self.w - 1) for _ in range(self.h)]
        self.vwalls = [[v] * (self.w) for _ in range(self.h - 1)]

    def genMaze(self, startX, startY):
        # start with all walls active
        self.setAllWalls(1)

        visited = [(startX, startY)]
        while len(visited) < self.w * self.h:
            pos = random.choice(visited)
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            random.shuffle(directions)
            for d in directions:
                px, py = pos
                dx, dy = d
                npx = px + dx
                npy = py + dy
                if not (npx, npy) in visited:
                    if 0 <= npx < self.w:
                        if 0 <= npy < self.h:
                            self.setWall(pos, (npx, npy), 0)
                            visited.append((npx, npy))
                            break

if __name__ == "__main__":
    maze = Maze()
    # maze.genRandomMazeWalls()
    maze.genMaze(0, 0)
    maze.printMaze()
