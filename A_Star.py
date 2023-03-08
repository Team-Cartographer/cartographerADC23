from PIL import Image
import heapq
from numpy import sqrt
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
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (h1 - h2) ** 2)


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

csv_path = fc.data_path + "/AStarRawData.csv"
csv_path = csv_path.replace("\\", "/")
with open(csv_path, mode="r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    full_list = list(csv_reader)


grid = full_list

final_path = astarfinal_path = astar(grid, (971, 940, get_height_and_slope(971, 940, grid)[0], get_height_and_slope(971, 940, grid)[1]),
                   (862, 1123, get_height_and_slope(862, 1123, grid)[0], get_height_and_slope(862, 1123, grid)[1]))
print("Final Path: ", final_path)


def add_pixel(img, x, y, color):
    img.putpixel((x, y), color)
    return img


def update_image(image_path: str, mvmt_path: list):
    path = image_path
    img = Image.open(path)
    color = (0, 0, 128)
    for i in range(len(mvmt_path)):
        x = mvmt_path[0]
        y = mvmt_path[1]
        img = add_pixel(img, x, y, color)
    img.save(fc.images_path + "/A_Star_heightmap.png")


try:
    update_image(fc.images_path + "/RAW_heightmap.png", final_path)
except TypeError:
    print("Image not updated. No path to draw.")
    pass
