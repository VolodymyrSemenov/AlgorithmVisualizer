import pygame

from Constants import *

class WindowState:
    def __init__(self, algorithm_visualizer):
        self.av = algorithm_visualizer

    def render_screen(self):
        pass

    def click(self):
        pass

    def what_is_clicked(self, position):
        pass

    def enter(self):
        pass

    def render_base(self):
        self.av.screen.fill(LIGHT_GRAY)
        for x in range(self.av.x):
            for y in range(self.av.y):
                pygame.draw.rect(self.av.screen, DARK_GRAY, pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
        for wall in self.av.walls:
            pygame.draw.rect(self.av.screen, BLACK, pygame.Rect(wall[0] * BLOCK_SIZE, wall[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def render_animation_base(self):
        self.render_base()
        self.render_start_stop()
        pygame.draw.rect(self.av.screen, BLACK, pygame.Rect(0, self.av.h - 50, self.av.buttonSize * 6, 50))

    def render_start_stop(self):
        pygame.draw.rect(self.av.screen, GREEN, pygame.Rect(self.av.start[0] * BLOCK_SIZE, self.av.start[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.av.screen, RED, pygame.Rect(self.av.end[0] * BLOCK_SIZE, self.av.end[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def render_completed_path(self, tick_rate):
        for path in self.av.completed_path:
            pygame.draw.rect(self.av.screen, EXTRA_DARK_GRAY, pygame.Rect(path[0] * BLOCK_SIZE, path[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            self.av.clock.tick(tick_rate)
            pygame.display.flip()