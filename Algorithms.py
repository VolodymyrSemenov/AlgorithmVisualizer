from collections import defaultdict
import colorsys
import math
import random
import heapq

def walls_to_edges(walls, x, y):
    complete_graph = []
    for i in range(x):
        for j in range(y - 1):
            complete_graph.append([(i, j), (i, j + 1)]) # Edge containing Node and Node below
    for i in range(x - 1):
        for j in range(y):
            complete_graph.append([(i, j), (i + 1, j)]) # Edge containing Node and Node right
    edges = defaultdict(list)
    for tile1, tile2 in complete_graph:
        if tile1 not in walls and tile2 not in walls:
            edges[tile1].append(tile2)
            edges[tile2].append(tile1)
    return edges

def prims_maze_gen(x, y, randomization_factor):
    DELTAS = [
        [0, 1],
        [0, -1],
        [-1, 0],
        [1, 0]
    ]
    walls = []
    visited = set()
    start_x, start_y = random.randint(1, x - 2), random.randint(1, y-2)
    visited.add((start_x, start_y))
    for dx, dy in DELTAS:
        walls.append((start_x + dx, start_y + dy))
    while walls:
        if random.randint(1, randomization_factor) == 1:
            random.shuffle(DELTAS)
        explored_wall = walls.pop()
        visited_around = []
        for dx, dy in DELTAS:
            neighboring_wall = (explored_wall[0] + dx, explored_wall[1] + dy)
            if neighboring_wall in visited:
                visited_around.append(neighboring_wall)
        if len(visited_around) == 1:
            visited.add(explored_wall)
            for dx, dy in DELTAS:
                new_wall = (explored_wall[0] + dx, explored_wall[1] + dy)
                if new_wall not in visited:
                    if new_wall[0] < 0 or new_wall[1] < 0 or new_wall[0] >= x or new_wall[1] >= y:
                        continue
                    walls.append(new_wall)

    walls = set()
    for i in range(x):
        for j in range(y):
            if (i, j) not in visited:
                walls.add((i, j))
    return walls


def kruskals_maze_gen(x, y):
    walls = set()
    for i in range(1, x, 2):
        for j in range(y):
            walls.add((i, j))
    for j in range(1, y, 2):
        for i in range(x):
            walls.add((i, j))

    removable_walls = []
    for wall in walls:
        if (wall[0] % 2 == 0 or wall[1] % 2 == 0) and (x % 2 == 1 or wall[0] != x-1) and (y % 2 == 1 or wall[1] != y-1):
            removable_walls.append(wall)
    node_sets = {}
    for i in range(x):
        for j in range(y):
            node = (i, j)
            if node not in walls:
                node_sets[node] = {node}
    random.shuffle(removable_walls)
    for wall in removable_walls:
        wall_x, wall_y = wall
        if wall_x % 2 == 1:
            tile_1 = (wall_x + 1, wall_y)
            tile_2 = (wall_x - 1, wall_y)
        else:
            tile_1 = (wall_x, wall_y + 1)
            tile_2 = (wall_x, wall_y - 1)
        set1 = node_sets[tile_1]
        set2 = node_sets[tile_2]
        if set1 != set2:
            if len(set1) > len(set2):
                node_sets[tile_1].update(set2)
                for tile in set2:
                    node_sets[tile] = node_sets[tile_1]
            else:
                node_sets[tile_2].update(set1)
                for tile in set1:
                    node_sets[tile] = node_sets[tile_2]
            walls.remove(wall)
    return walls


def depth_first_search(edges, start, end, full_explore):
    stack = [start]
    ordered_visited_nodes = [start]
    visited = set()
    depth = {start: 0}
    discovered_node = {start: None}
    while stack and (end not in visited or full_explore):
        node_exploring = stack.pop()
        connected_nodes = edges[node_exploring]
        random.shuffle(connected_nodes)
        for node in connected_nodes:
            if node not in visited and (end not in visited or full_explore):
                depth[node] = depth[node_exploring] + 1
                discovered_node[node] = node_exploring
                visited.add(node)
                ordered_visited_nodes.append(node)
                stack.append(node)

    completed_path = []
    current_node = discovered_node.get(end)
    if current_node:
        for i in range(depth[end] - 1):
            completed_path.append(current_node)
            current_node = discovered_node[current_node]
    return depth, completed_path, ordered_visited_nodes


def a_star_search(edges, start, end, full_explore, heurisitic_weight):
    ordered_visited_nodes = [start]
    visited = set()
    depth = {start: 0}
    cost_function = lambda point: depth[point] + (abs((point[0] - end[0])) + abs(point[1] - end[1])) * heurisitic_weight
    queue = PriorityQueue(cost_function, [start])
    depth[start] = 0
    discovered_node = {start: None}
    while len(queue.heap) != 0 and (end not in visited or full_explore):
        node_exploring = queue.pop()
        for node in edges[node_exploring]:
            if node not in visited and (end not in visited or full_explore):
                depth[node] = depth[node_exploring] + 1
                discovered_node[node] = node_exploring
                visited.add(node)
                ordered_visited_nodes.append(node)
                queue.add(node)

    completed_path = []
    current_node = discovered_node.get(end)
    if current_node:
        for i in range(depth[end] - 1):
            completed_path.append(current_node)
            current_node = discovered_node[current_node]

    return depth, completed_path, ordered_visited_nodes


def hsv_to_rgb(h, s, v, m):
    r, g, b = colorsys.hsv_to_rgb(h/360 * m, s, v)
    r = math.floor(r * 255)
    g = math.floor(g * 255)
    b = math.floor(b * 255)
    return r, g, b


def two_random_coord(x, y): # In Different Quads
    x_coord_bound = x // 2
    vertical_coord = y // 2
    x1 = random.randint(0, x_coord_bound - 1)     # Left half
    x2 = random.randint(x_coord_bound, x - 1)     # Right Half
    y1 = random.randint(0, vertical_coord - 1)    # Upper Half
    y2 = random.randint(vertical_coord, y - 1)    # Lower Half
    match random.randint(0, 3): # To get any arrangement
        case 0:
            return (x1, y1), (x2, y2)
        case 1:
            return (x2, y2), (x1, y1)
        case 2:
            return (x1, y2), (x2, y1)
        case 3:
            return (x2, y1), (x1, y2)


class PriorityQueue:
    def __init__(self, weight_function, elements):
        self.heap = [(weight_function(x), x) for x in elements]
        heapq.heapify(self.heap)
        self.weight_function = weight_function

    def add(self, element):
        heapq.heappush(self.heap, (self.weight_function(element), element))

    def pop(self):
        return heapq.heappop(self.heap)[1]
