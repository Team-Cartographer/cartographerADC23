from PIL import Image
import heapq
from numpy import sqrt
from utils import show_warning, timeit, load_json
from ui import get_pathfinding_endpoints
import FileManager as fm
from tqdm import tqdm


class Node:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y

        self.parent = parent

        self.height = grid[y][x][2]
        self.slope = grid[y][x][3]

        self.g = 0
        self.h = 0
        self.f = 0

        if parent is not None:
            self.g = parent.new_g(self)
            self.h = self.heuristic(goal_node)
            self.f = self.g + self.h

    def __lt__(self, other):
        return self.f < other.f

    def heuristic(self, other):
        return self.dist_btw(other)

    def dist_btw(self, other):
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.h - other.h) ** 2)

    def new_g(self, other) -> float:
        # constant values:
        k_dist = 1
        k_slope = 0.25

        slope_penalty = 0  # we could perhaps allow the user to change how much they want to penalize slopes #
        if other.slope >= 20:
            slope_penalty = 25
        elif other.slope >= 8:
            slope_penalty = 5  # see above to do

        dist = self.dist_btw(other)
        slope = abs(self.slope - other.slope)

        eqn = k_dist * dist + k_slope * slope + slope_penalty
        return eqn


@timeit
def astar():
    nodes = []

    heapq.heappush(nodes, start_node)
    visited = set()

    with tqdm(total=None, desc='A* algorithm', unit=" Nodes") as pbar:
        while nodes:
            current = heapq.heappop(nodes)

            if (current.x, current.y) in visited:
                continue
            visited.add((current.x, current.y))

            if current.x == goal_node.x and current.y == goal_node.y and current.height == goal_node.height:
                path = []
                while current.parent:
                    path.append((current.x, current.y, current.height))
                    current = current.parent
                path.append((start_node.x, start_node.y, start_node.height))
                path.reverse()
                return path

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                x2 = current.x + dx
                y2 = current.y + dy

                if 0 <= x2 < len(grid) and 0 <= y2 < len(grid[0]):
                    new_node = Node(x2, y2, current)
                    heapq.heappush(nodes, new_node)

            pbar.update()
    return None


def update_image(image_path: str, mvmt_path: list):
    path = image_path
    img = Image.open(path)

    color = (255, 0, 0)
    for i in tqdm(range(len(mvmt_path)), desc="Updating image"):
        x = mvmt_path[i][0]
        y = mvmt_path[i][1]
        img.putpixel((x, y), color)

    img.save(fm.images_path + "/AStar_Path.png")


def div_10_points(final_path : list) -> list:
    comm_points = []
    dist = round(len(final_path) / 11)
    for i in range(11):
        comm_points.append(final_path[i * dist])

    comm_points.pop(0)
    return comm_points


def line_to_earth(x, y):
    m = (y-1250)/(x-638)
    b = -m*x + y
    return int(m), int(b)


if __name__ == "__main__":

    (start_x, start_y), (goal_x, goal_y) = get_pathfinding_endpoints(fm.get_size_constant(), fm.images_path)

    grid = load_json(fm.data_path + "/AStarRawData.json")

    # Testing. To be removed later
    # start_x, start_y = 0, 0
    # goal_x, goal_y = 100, 100

    start_node = Node(start_x, start_y)
    goal_node = Node(goal_x, goal_y)

    final_path = astar()

    if final_path is not None:
        update_image(fm.images_path + '/moon_surface_texture.png', final_path)
    else:
        show_warning("A* Pathfinding Error", "No Valid Path found between points.")

    # For Relative Earth position Pathfinding Calculation ---
    divided_points = div_10_points(final_path)

    m, b = line_to_earth(divided_points[0][0], divided_points[0][2])
    # Slope of a line spanning from a point to the relative position of earth.
    print(f'y = {m}x + {b}')


