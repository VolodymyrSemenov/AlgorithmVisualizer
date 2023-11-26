import pygame
from pygame.locals import *

from DrawingState import DrawingState, Tool
from VisualizationState import VisualizationState, Algo
from AnimationState import AnimationState
from Constants import *


class AlgorithmVisualizer:
    def __init__(self, x, y):
        pygame.init()
        pygame.font.init()
        self.big_font = pygame.font.Font("Resources/font.ttf", 35)
        self.small_font = pygame.font.Font("Resources/font.ttf", 15)

        # Screen Config
        self.x = x
        self.y = y
        self.w = x * BLOCK_SIZE
        self.h = y * BLOCK_SIZE + 50
        self.buttonSize = self.w // 6

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.w, self.h), pygame.RESIZABLE)
        pygame.display.set_caption('Algorithm Visualizer')

        # Control Config
        self.mouseDown = False

        # Tile and Coloring Config
        self.walls = set()
        self.start = (self.x // 4, self.y // 2)
        self.end = (self.x * 3 // 4, self.y // 2)
        self.depths = {}
        self.completed_path = []
        self.maxDepth = 0
        self.rainbow_speed_multiplier = 1
        self.ordered_visited_nodes = []
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
                elif event.type == VIDEORESIZE:
                    self.switch_drawing_state()
                    self.w, self.h = pygame.display.get_window_size()
                    self.x = self.w // BLOCK_SIZE
                    self.y = (self.h - 50) // BLOCK_SIZE
                    self.w = self.x * BLOCK_SIZE
                    self.h = self.y * BLOCK_SIZE + 50
                    self.buttonSize = self.w // 6
                    self.screen = pygame.display.set_mode((self.w, self.h), pygame.RESIZABLE)
                    self.hard_clear()
                if self.mouseDown:
                  self.state.click()
            self.state.render_screen()
            self.clock.tick(60)

    def switch_drawing_state(self):
        self.state = DrawingState(self)

    def switch_visualization_state(self):
        self.state = VisualizationState(self)

    def switch_animation_state(self):
        self.state = AnimationState(self)

