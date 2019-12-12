import pprint
import numpy as np
import itertools
import math

class Point():
    def __init__(self, col, row):
        self.col = col
        self.row = row

class Map():
    def __init__(self, map, grid):
        self.map = map
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.observableAsteroids = np.zeros((self.rows, self.cols))

def print2DArray(matrix: list):
    for row in matrix:
        print(row)

def splitInnerLists(matrix: list) -> list:
    for row in range(len(matrix)):
        matrix[row] = [char for char in matrix[row][0]]
    return matrix

def prepareMap(path: str) -> list:
    with open(path) as textFile:
        matrix = [line.split() for line in textFile]
    matrix = splitInnerLists(matrix)
    return matrix

def createGridFromMap(map: list) -> np.ndarray:
    rows = len(map)
    cols = len(map[0])

    grid = np.zeros((rows, cols))
    for row, col in itertools.product(range(rows), range(cols)):
        if map[row][col] == '#':
            grid[row][col] = 1
    return grid

def linearFunction(scalingFactor: float, col: int, startPoint: Point):
    b = startPoint.row - scalingFactor*startPoint.col
    return scalingFactor*col + b

def computeScalingFactor(startPoint: Point, endPoint: Point):
    if endPoint.col == startPoint.col:
        if endPoint.row < startPoint.row:
            return ("verticalup")
        elif endPoint.row > startPoint.row:
            return ("verticaldown")
    return (endPoint.row - startPoint.row)/(endPoint.col - startPoint.col)

def outOfBounds(y: float, map: Map, startPoint: Point, endPoint: Point) -> bool: 
    if startPoint.row < endPoint.row:
        if y < startPoint.row or y > endPoint.row:
            return True
    elif startPoint.row > endPoint.row:
        if y < endPoint.row or y > startPoint.row:
            return True
    return False

def computeNorm(startPoint: Point, endPoint: Point) -> float:
    return math.sqrt((endPoint.col - startPoint.col)**2 + (endPoint.row - startPoint.row)**2)

def checkIfClosestObservablePointOnLine(startPoint:Point, endPoint: Point, observablePoints: list) -> bool:
    lenToPoint = computeNorm(startPoint, endPoint)
    for row, col in observablePoints:
        end = Point(col, row)
        distance = computeNorm(startPoint, end)
        if distance < lenToPoint:
            return False
    return True

def checkIfAsteroidIsObservable(startPoint: Point, endPoint: Point, map: Map) -> bool:
    scalingFactor = computeScalingFactor(startPoint, endPoint)
    observablePointsFromPoint = []
    if scalingFactor == "verticalup":
        observablePointsFromPoint = [(row, startPoint.col) for row in range(map.rows) \
                                        if map.grid[row][startPoint.col] == 1 \
                                        and startPoint.row != row \
                                        and row < startPoint.row]
    elif scalingFactor == "verticaldown":
        observablePointsFromPoint = [(row, startPoint.col) for row in range(map.rows) \
                                        if map.grid[row][startPoint.col] == 1 \
                                        and startPoint.row != row \
                                        and row > startPoint.row]
    else:
        for col in range(map.cols):
            if col == startPoint.col:
                continue
            row = linearFunction(scalingFactor, col, startPoint)
            if outOfBounds(row, map, startPoint, endPoint):
                continue
            if isinstance(row, int):
                if map.grid[row][col] == 1:
                    observablePointsFromPoint.append((int(row), col))
            elif row.is_integer():
                if map.grid[int(row)][col] == 1:
                    observablePointsFromPoint.append((int(row), col))
    return checkIfClosestObservablePointOnLine(startPoint, endPoint, observablePointsFromPoint)                

def findAllObservableAsteroidsFromPoint(point: Point):
    countObservableAsteroids = 0
    for row, col in itertools.product(range(map.rows), range(map.cols)):
        if map.grid[row][col] == 0:
            continue
        if row == point.row and col == point.col:
            continue
        endPoint = Point(col, row)
        observable = checkIfAsteroidIsObservable(point, endPoint, map)
        if observable:
            countObservableAsteroids += 1
    if countObservableAsteroids == 0:
        print('Im nothing')
        print(point.col, point.row)
    return countObservableAsteroids

def computeObservableAsteroids(map: Map) -> int:
    for row, col in itertools.product(range(map.rows), range(map.cols)):
        if map.grid[row][col] == 0:
            continue
        startPoint = Point(col, row)
        map.observableAsteroids[row][col] = findAllObservableAsteroidsFromPoint(startPoint)
    return map
temp_map = prepareMap('dec10/map.txt')
grid = createGridFromMap(temp_map)

map = Map(temp_map, grid)

result = computeObservableAsteroids(map)
print(map.observableAsteroids)
print('end')

