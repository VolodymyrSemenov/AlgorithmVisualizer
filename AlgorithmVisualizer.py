import pygame
from pygame.locals import *

from DrawingState import DrawingState, Tool
from VisualizationState import VisualizationState, Algo
from BFSState import BFSState
from DFSState import DFSState
from AStarState import AStateState
from Constants import *


class AlgorithmVisualizer:
    def __init__(self, x=49, y=31):
        pygame.init()
        pygame.font.init()
        self.big_font = pygame.font.Font("Resources/font.ttf", 35)
        self.small_font = pygame.font.Font("Resources/font.ttf", 15)

        # Screen Config
        self.x = x
        self.y = y
        self.w = x * BLOCK_SIZE
        self.h = y * BLOCK_SIZE + 50
        self.buttonSize = self.w / 6

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Algorithm Visualizer')

        # Control Config
        self.mouseDown = False
        self.drawingTool = Tool.WALL
        self.selectedAlgo = Algo.BREADTH_FIRST_SEARCH
        self.fullExplore = False

        # Tile and Coloring Config
        self.walls = set()
        self.start = (self.x // 4, self.y // 2)
        self.end = (self.x * 3 // 4, self.y // 2)
        self.depths = {}
        self.completed_path = []
        self.maxDepth = 0
        self.rainbow_speed_multiplier = 1
        self.ordered_visited_nodes = []

        self.drawing_state_big_text = self.big_font.render("WALLS         START            END          ERASER                               NEXT", True, BLACK)
        self.drawing_state_small_text1 = self.small_font.render("GENERATE MAZE", True, BLACK)
        self.drawing_state_small_text2 = self.small_font.render("100%  90%  80%   70%  CLR", True, BLACK)
        self.visualization_state_big_text = self.big_font.render("BFS              DFS                                MAP ALL         EDIT             NEXT", True, BLACK)
        self.visualization_state_small_text1 = self.small_font.render("A*", True, BLACK)
        self.visualization_state_small_text2 = self.small_font.render("Optimal             Fast", True, BLACK)
        self.state = DrawingState(self)

        self.run()

    def clear_tiles(self):
        self.depths = {}
        self.completed_path = []
        self.maxDepth = 0

    def hard_clear(self):
        self.walls = set()
        self.start = (self.x // 4, self.y // 2)
        self.end = (self.x * 3 // 4, self.y // 2)
        self.depths = {}
        self.completed_path = []
        self.maxDepth = 0
        self.rainbow_speed_multiplier = 1

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    self.mouseDown = True
                elif event.type == MOUSEBUTTONUP:
                    self.mouseDown = False
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        self.state.enter()
                    elif event.key == K_ESCAPE:
                        quit()
                elif event.type == QUIT:
                    quit()
                if self.mouseDown:
                    self.state.click()
            self.state.render_screen()

    def switch_drawing_state(self):
        self.state = DrawingState(self)

    def switch_visualization_state(self):
        self.state = VisualizationState(self)

    def switch_bfs_state(self):
        self.state = BFSState(self)

    def switch_dfs_state(self):
        self.state = DFSState(self)

    def switch_astar_state(self):
        self.state = AStateState(self)
