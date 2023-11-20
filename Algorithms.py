from collections import deque, defaultdict
import colorsys
import math
from random import shuffle
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


def perfect_maze_gen(x, y):
    walls = set()
    for i in range(1, x, 2):
        for j in range(y):
            walls.add((i, j))
    for j in range(1, y, 2):
        for i in range(x):
            walls.add((i, j))

    removable_walls = []
    for wall in walls:
        if not (wall[0] % 2 == 1 and wall[1] % 2 == 1):
            removable_walls.append(wall)
    node_sets = walls_to_node_sets(walls, x, y)
    random.shuffle(removable_walls)
    for wall in removable_walls:
        wall_x, wall_y = wall
        if wall_x % 2 == 1:
            tile_1 = (wall_x + 1, wall_y)
            tile_2 = (wall_x - 1, wall_y)
        else:
            tile_1 = (wall_x, wall_y + 1)
            tile_2 = (wall_x, wall_y - 1)
        new_node_sets = []
        combined_node_set = []
        for node_set in node_sets:
            if tile_1 in node_set or tile_2 in node_set:
                combined_node_set.append(node_set)
            else:
                new_node_sets.append(node_set)
        if len(combined_node_set) != 1:
            new_node_sets.append(combined_node_set[0].union(combined_node_set[1]))
            walls.remove(wall)
        else:
            new_node_sets.append(combined_node_set[0])
        node_sets = new_node_sets
    return walls


def imperfect_maze_gen(x, y, percent):
    walls = list(perfect_maze_gen(x, y))
    shuffle(walls)
    return set(walls[math.floor(len(walls) * percent):])


def walls_to_node_sets(walls, x, y):
    all_nodes = []
    for i in range(x):
        for j in range(y):
            all_nodes.append((i, j))
    filtered_nodes = list()
    for node in all_nodes:
        if node not in walls:
            filtered_nodes.append({node})
    return filtered_nodes


def breadth_first_search(edges, start, end, full_explore):
    queue = deque()
    queue.append(start)
    visited_nodes = [start]
    depth = {start: 0}
    discovered_node = {start: None}
    while queue and (end not in visited_nodes or full_explore):
        node_exploring = queue.popleft()
        for node in edges[node_exploring]:
            if node not in visited_nodes and (end not in visited_nodes or full_explore):
                depth[node] = depth[node_exploring] + 1
                discovered_node[node] = node_exploring
                visited_nodes.append(node)
                queue.append(node)

    completed_path = []
    current_node = discovered_node.get(end)
    if current_node:
        for i in range(depth[end] - 1):
            completed_path.append(current_node)
            current_node = discovered_node[current_node]
    return depth, completed_path


def depth_first_search(edges, start, end, full_explore):
    stack = [start]
    visited_nodes = [start]
    depth = {start: 0}
    discovered_node = {start: None}
    while stack and (end not in visited_nodes or full_explore):
        node_exploring = stack.pop()
        connected_nodes = edges[node_exploring]
        random.shuffle(connected_nodes)
        for node in connected_nodes:
            if node not in visited_nodes and (end not in visited_nodes or full_explore):
                depth[node] = depth[node_exploring] + 1
                discovered_node[node] = node_exploring
                visited_nodes.append(node)
                stack.append(node)

    completed_path = []
    current_node = discovered_node.get(end)
    if current_node:
        for i in range(depth[end] - 1):
            completed_path.append(current_node)
            current_node = discovered_node[current_node]
    return depth, completed_path, visited_nodes


def a_star_search(edges, start, end, full_explore, optimal):
    visited_nodes = [start]
    depth = {start: 0}
    if optimal:
        cost_function = lambda point: depth[point] + (abs((point[0] - end[0])) + abs(point[1] - end[1]))
    else:
        cost_function = lambda point: depth[point] + (abs((point[0] - end[0])) + abs(point[1] - end[1])) * 1.5
    queue = PriorityQueue(cost_function, [start])
    depth[start] = 0
    discovered_node = {start: None}
    while len(queue.heap) != 0 and (end not in visited_nodes or full_explore):
        node_exploring = queue.pop()
        for node in edges[node_exploring]:
            if node not in visited_nodes and (end not in visited_nodes or full_explore):
                depth[node] = depth[node_exploring] + 1
                discovered_node[node] = node_exploring
                visited_nodes.append(node)
                queue.add(node)


    completed_path = []
    current_node = discovered_node.get(end)
    if current_node:
        for i in range(depth[end] - 1):
            completed_path.append(current_node)
            current_node = discovered_node[current_node]
    return depth, completed_path, visited_nodes


def hsv_to_rgb(h, s, v, m):
    r, g, b = colorsys.hsv_to_rgb(h/360 * m, s, v)
    r = math.floor(r * 255)
    g = math.floor(g * 255)
    b = math.floor(b * 255)
    return r, g, b


def two_random_even_coord(x, y):
    x_coord_bound = x // 4
    vertical_coord = y // 4
    x1 = random.randint(1, x_coord_bound - 1) * 2 # Left half
    x2 = random.randint(x_coord_bound, x // 2) * 2 # Right Half
    y1 = random.randint(1, vertical_coord - 1) * 2 # Upper Half
    y2 = random.randint(vertical_coord, y // 2) * 2 # Lower Half
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
