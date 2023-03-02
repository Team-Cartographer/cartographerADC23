import heapq

# Quadtree node class
class QuadNode:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.children = [None, None, None, None]
        self.items = []

    def split(self):
        child_width = self.width // 2
        child_height = self.height // 2
        self.children[0] = QuadNode(self.x, self.y, child_width, child_height)
        self.children[1] = QuadNode(self.x + child_width, self.y, child_width, child_height)
        self.children[2] = QuadNode(self.x, self.y + child_height, child_width, child_height)
        self.children[3] = QuadNode(self.x + child_width, self.y + child_height, child_width, child_height)

    def insert(self, item):
        if not self.contains(item):
            return False
        if len(self.items) < 4:
            self.items.append(item)
            return True
        if not self.children[0]:
            self.split()
        for child in self.children:
            if child.insert(item):
                return True
        return False

    def contains(self, item):
        x, y = item
        return self.x <= x < self.x + self.width and self.y <= y < self.y + self.height

    def find_items(self, rect):
        if not self.intersects(rect):
            return []
        result = [item for item in self.items if rect.contains(item)]
        if self.children[0]:
            for child in self.children:
                result.extend(child.find_items(rect))
        return result

    def intersects(self, rect):
        return self.x < rect.right and self.right > rect.x and self.y < rect.bottom and self.bottom > rect.y

    @property
    def right(self):
        return self.x + self.width

    @property
    def bottom(self):
        return self.y + self.height


# Helper function to get the neighbors of a node
def get_neighbors(grid, node):
    x, y = node
    neighbors = []
    # Check left
    if x > 0 and grid[y][x-1] == 0:
        neighbors.append((x-1, y))
    # Check right
    if x < len(grid[0]) - 1 and grid[y][x+1] == 0:
        neighbors.append((x+1, y))
    # Check up
    if y > 0 and grid[y-1][x] == 0:
        neighbors.append((x, y-1))
    # Check down
    if y < len(grid) - 1 and grid[y+1][x] == 0:
        neighbors.append((x, y+1))
    return neighbors

# A* search algorithm using a quadtree
def astar_quadtree(grid, start, goal):
    pq = []  # Priority queue for open nodes
    visited = set()  # Set of visited nodes
    parents = {}  # Dictionary of parents for each node
    g_score = {start: 0}  # Dictionary of g-scores for each node

    # Initialize the priority queue with the start node
    f_score = g_score[start] + heuristic(start, goal)
    heapq.heappush(pq, (f_score, start))

    while pq:
        # Pop the node with the lowest f-score
        current = heapq.heappop(pq)[1]

        if current == goal:
            # Reconstruct and return the path
            path = [current]
            while current in parents:
                current = parents[current]
                path.append(current)
            path.reverse()
            return path

        visited.add(current)
        for neighbor in get_neighbors(grid, current):
            if neighbor in visited:
                continue

            # Calculate the tentative g-score for the neighbor
            tentative_g_score = g_score[current] + 1

            # If the neighbor is not in the priority queue, add it
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                parents[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score = g_score[neighbor] + heuristic(neighbor, goal)
                heapq.heappush(pq, (f_score, neighbor))

    # If there is no path to the goal, return None
    return None

# Helper function to calculate the heuristic distance between two nodes
def heuristic(node1, node2):
    return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])

# Test scenarios
grid = [
    [0, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 1],
    [0, 0, 0, 0]
]

start = (0, 0)
goal = (0, 3)
path = astar_quadtree(grid, start, goal)
print(path) # [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (2, 3), (1, 3), (0, 3)]

