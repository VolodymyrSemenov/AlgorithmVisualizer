import pygame
from Constants import *

class State:
    def __init__(self, algorithm_visualizer):
        self.av = algorithm_visualizer

    def render_screen(self):
        pass

    def click(self):
        pass

    def enter(self):
        pass

    def scale_text(self, rendered_text):
        default_size = [1176, 794]
        actual_size = pygame.display.get_window_size()
        return pygame.transform.scale_by(rendered_text, (actual_size[0] / default_size[0], actual_size[0] / default_size[0]))

    def render_base(self):
        self.av.screen.fill(LIGHT_GRAY)
        for x in range(self.av.x):
            for y in range(self.av.y):
                pygame.draw.rect(self.av.screen, DARK_GRAY, pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
        for wall in self.av.walls:
            pygame.draw.rect(self.av.screen, BLACK, pygame.Rect(wall[0] * BLOCK_SIZE, wall[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        self.render_start_stop()


    def render_start_stop(self):
        pygame.draw.rect(self.av.screen, GREEN, pygame.Rect(self.av.start[0] * BLOCK_SIZE, self.av.start[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.av.screen, RED, pygame.Rect(self.av.end[0] * BLOCK_SIZE, self.av.end[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
