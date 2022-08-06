from Algorithms import breadth_first_search, depth_first_search, a_star_search, walls_to_edges, hsv_to_rgb
import math
import pygame
from enum import Enum
from State import WindowState
from Constants import *


class Algo(Enum):
    BREADTH_FIRST_SEARCH = 1
    DEPTH_FIRST_SEARCH = 2
    A_STAR_SEARCH = 3
    A_STAR_SEARCH_FAST = 4


class VisualizationState(WindowState):
    def __init__(self, algorithm_visualizer):
        self.av = algorithm_visualizer

    def render_screen(self):
        self.av.screen.fill(LIGHT_GRAY)
        for x in range(self.av.x):
            for y in range(self.av.y):
                pygame.draw.rect(self.av.screen, DARK_GRAY, pygame.Rect(x * BLOCKSIZE, y * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE), 1)
        for coordinate, depth in self.av.depths.items():
            pygame.draw.rect(self.av.screen, hsv_to_rgb(depth, 1, 1, self.av.rainbow_speed_multiplier), pygame.Rect(coordinate[0] * BLOCKSIZE, coordinate[1] * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE))
        for wall in self.av.walls:
            pygame.draw.rect(self.av.screen, BLACK, pygame.Rect(wall[0] * BLOCKSIZE, wall[1] * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE))
        for i in range(6):
            pygame.draw.rect(self.av.screen, DARK_GRAY, pygame.Rect(i * self.av.buttonSize, self.av.h - 50, self.av.buttonSize, 50), 2)
        for i in range(2):
            pygame.draw.rect(self.av.screen, DARK_GRAY, pygame.Rect(self.av.buttonSize * 2 + i * self.av.buttonSize / 2, self.av.h - 25, self.av.buttonSize / 2, 25), 2)
        for path in self.av.completed_path:
            pygame.draw.rect(self.av.screen, XDARK_GRAY, pygame.Rect(path[0] * BLOCKSIZE, path[1] * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE))
        pygame.draw.rect(self.av.screen, GREEN, pygame.Rect(self.av.start[0] * BLOCKSIZE, self.av.start[1] * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE))
        pygame.draw.rect(self.av.screen, RED, pygame.Rect(self.av.end[0] * BLOCKSIZE, self.av.end[1] * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE))
        self.av.screen.blit(self.av.visualization_state_big_text, [75, self.av.h - 45])
        self.av.screen.blit(self.av.visualization_state_small_text1, [480, self.av.h - 45])
        self.av.screen.blit(self.av.visualization_state_small_text2, [420, self.av.h - 20])
        pygame.display.flip()

    def click(self):
        self.what_is_clicked(pygame.mouse.get_pos())

    def what_is_clicked(self, mouse_position):
        mouse_x, mouse_y = mouse_position
        if mouse_y < self.av.h - 50:
            return math.floor(mouse_x / BLOCKSIZE), math.floor(mouse_y / BLOCKSIZE)
        else:
            button = math.floor(mouse_x / self.av.buttonSize) + 1
            if button == 1:
                if self.av.selectedAlgo != Algo.BREADTH_FIRST_SEARCH:
                    self.av.clear_tiles()
                self.av.selectedAlgo = Algo.BREADTH_FIRST_SEARCH
            elif button == 2:
                if self.av.selectedAlgo != Algo.DEPTH_FIRST_SEARCH:
                    self.av.clear_tiles()
                self.av.selectedAlgo = Algo.DEPTH_FIRST_SEARCH
            elif button == 3:
                if (mouse_x - 2 * self.av.buttonSize) < self.av.buttonSize / 2:
                    if self.av.selectedAlgo != Algo.A_STAR_SEARCH:
                        self.av.clear_tiles()
                        self.av.selectedAlgo = Algo.A_STAR_SEARCH
                else:
                    if self.av.selectedAlgo != Algo.A_STAR_SEARCH_FAST:
                        self.av.clear_tiles()
                        self.av.selectedAlgo = Algo.A_STAR_SEARCH_FAST
            elif button == 4:
                self.av.fullExplore = not self.av.fullExplore
            elif button == 5:
                self.av.clear_tiles()
                self.av.switch_drawing_state()
            elif button == 6:
                self.enter()
        return -1, -1

    def enter(self):
        if self.av.selectedAlgo == Algo.BREADTH_FIRST_SEARCH:
            drawing_edges = walls_to_edges(self.av.walls, self.av.x, self.av.y)
            self.av.maxDepth, self.av.depths, self.av.completed_path = breadth_first_search(drawing_edges, self.av.start, self.av.end, self.av.fullExplore)
            self.av.rainbow_speed_multiplier = math.floor(300 / self.av.maxDepth)
            if self.av.rainbow_speed_multiplier < 0.0001:
                self.av.rainbow_speed_multiplier = 1
            self.av.switch_animation_bfs_state()

        if self.av.selectedAlgo == Algo.DEPTH_FIRST_SEARCH:
            drawing_edges = walls_to_edges(self.av.walls, self.av.x, self.av.y)
            self.av.maxDepth, self.av.depths, self.av.completed_path, self.av.ordered_visited_nodes = depth_first_search(drawing_edges, self.av.start, self.av.end, self.av.fullExplore)
            self.av.rainbow_speed_multiplier = math.floor(300 / self.av.maxDepth)
            if self.av.rainbow_speed_multiplier < 0.0001:
                self.av.rainbow_speed_multiplier = 1
            self.av.switch_animation_dfs_state()

        if self.av.selectedAlgo == Algo.A_STAR_SEARCH:
            drawing_edges = walls_to_edges(self.av.walls, self.av.x, self.av.y)
            self.av.maxDepth, self.av.depths, self.av.completed_path, self.av.ordered_visited_nodes = a_star_search(drawing_edges, self.av.start, self.av.end, self.av.fullExplore, True)
            self.av.rainbow_speed_multiplier = math.floor(300 / self.av.maxDepth)
            if self.av.rainbow_speed_multiplier < 0.0001:
                self.av.rainbow_speed_multiplier = 1
            self.av.switch_animation_astar_state()

        if self.av.selectedAlgo == Algo.A_STAR_SEARCH_FAST:
            drawing_edges = walls_to_edges(self.av.walls, self.av.x, self.av.y)
            self.av.maxDepth, self.av.depths, self.av.completed_path, self.av.ordered_visited_nodes = a_star_search(drawing_edges, self.av.start, self.av.end, self.av.fullExplore, False)
            self.av.rainbow_speed_multiplier = math.floor(300 / self.av.maxDepth)
            self.av.switch_animation_astar_state()
