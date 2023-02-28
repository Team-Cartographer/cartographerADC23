from PIL import Image
import heapq
import math
import csv
from ast import literal_eval
import FolderCreator as fc


class Node:
    def __init__(self, x, y, height, f, g, h, parent=None):
        self.x = x
        self.y = y
        self.height = height
        self.f = f
        self.g = g
        self.h = h
        self.parent = parent

    def __lt__(self, other):
        return self.f < other.f


def get_height_and_slope(x, y, grid):
    temp = (grid[x][y])
    temp = literal_eval(temp)
    if temp == 0:

        print(temp)
        print(x, y)
        print(grid[x])
    return float(temp[2]), float(temp[3])


def distBtw(x1, y1, h1, x2, y2, h2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (h1 - h2) ** 2)


def heuristic(x1, y1, x2, y2, h1, h2):
    heur_rtn = distBtw(x1, y1, h1, x2, y2, h2)
    return heur_rtn


def astar(grid, start, goal):
    nodes = []
    heapq.heappush(nodes, Node(start[0], start[1], start[2], 0, 0, 0))
    visited = set()

    while nodes:
        current = heapq.heappop(nodes)

        if (current.x, current.y) in visited:
            continue
        visited.add((current.x, current.y))

        if current.x == goal[0] and current.y == goal[1] and current.height == goal[2]:
            path = []
            while current.parent:
                path.append((current.x, current.y, current.height))
                current = current.parent
            path.append((start[0], start[1], start[2]))
            path.reverse()
            return path

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            x2 = current.x + dx
            y2 = current.y + dy
            if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]):
                h2, slope = get_height_and_slope(x2, y2, grid)
                if slope <= 20:
                    g = current.g + distBtw(float(current.x), float(current.y), float(current.height), float(x2), float(y2), float(h2))
                    h = heuristic(x2, y2, goal[0], goal[1], h2, goal[2])
                    f = g + h
                    heapq.heappush(nodes, Node(x2, y2, h2, f, g, h, current))
        print((len(visited))/(1277 ** 2), "% complete. Visited ", len(visited), " nodes")
    return None

# Test Case

csv_path = os.getcwd() + "/Processed Data/Astar Data.csv"
csv_path = csv_path.replace("\\", "/")
with open(csv_path, mode="r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    full_list = list(csv_reader)


grid = full_list

final_path = astar(grid, (950, 343, get_height_and_slope(950, 343, grid)[0],
                          get_height_and_slope(950, 343, grid)[1]), (3, 287, -19.375, 13.0))
print("Final Path: ", final_path)

data_path = os.getcwd() + "/Processed Data/Rectangular Coordinate Data.csv"
data_path = data_path.replace("\\", "/")
with open(data_path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    data_list = list(csv_reader)


def add_pixel(img, x, y, color):
    img.putpixel((x, y), color)
    return img


def update_image(x, y):
    path = "C:/Users/Owner/Desktop/heightmap_test1.jpg"
    img = Image.open(path)
    color = (255, 0, 0)

    img = add_pixel(img, x, y, color)
    img.save(path)


for i in range(len(final_path)):
    update_image(final_path[i][0], final_path[i][1])
