from State import WindowState
from Algorithms import hsv_to_rgb
from Constants import *
import pygame


class AnimationBFSState(WindowState):
    def __init__(self, algorithm_visualizer):
        self.av = algorithm_visualizer

    def what_is_clicked(self, position):
        pass

    def click(self):
        pass

    def enter(self):
        pass

    def render_screen(self):
        self.av.screen.fill(LIGHT_GRAY)
        for x in range(self.av.x):
            for y in range(self.av.y):
                pygame.draw.rect(self.av.screen, DARK_GRAY, pygame.Rect(x * BLOCKSIZE, y * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE), 1)
        for wall in self.av.walls:
            pygame.draw.rect(self.av.screen, BLACK, pygame.Rect(wall[0] * BLOCKSIZE, wall[1] * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE))
        pygame.draw.rect(self.av.screen, BLACK, pygame.Rect(0, self.av.h - 50, self.av.buttonSize * 6, 50))
        pygame.draw.rect(self.av.screen, GREEN, pygame.Rect(self.av.start[0] * BLOCKSIZE, self.av.start[1] * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE))
        pygame.draw.rect(self.av.screen, RED, pygame.Rect(self.av.end[0] * BLOCKSIZE, self.av.end[1] * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE))

        for i in range(1, self.av.maxDepth + 1):
            for coordinate, depth in self.av.depths.items():
                if depth == i:
                    pygame.draw.rect(self.av.screen, hsv_to_rgb(depth, 1, 1, self.av.rainbow_speed_multiplier), pygame.Rect(coordinate[0] * BLOCKSIZE, coordinate[1] * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE))
                    pygame.draw.rect(self.av.screen, RED, pygame.Rect(self.av.end[0] * BLOCKSIZE, self.av.end[1] * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE))
            self.av.clock.tick(10)
            pygame.display.flip()

        for path in self.av.completed_path:
            pygame.draw.rect(self.av.screen, XDARK_GRAY, pygame.Rect(path[0] * BLOCKSIZE, path[1] * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE))
            self.av.clock.tick(50)
            pygame.display.flip()

        self.av.colorings = self.av.depths
        self.av.switch_visualization_state()
