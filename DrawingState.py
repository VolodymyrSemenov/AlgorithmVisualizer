import pygame
from enum import Enum

from Algorithms import imperfect_maze_gen, two_random_even_coord
from State import WindowState
from Constants import *


class Tool(Enum):
    WALL = 1
    START = 2
    END = 3
    ERASER = 4


class DrawingState(WindowState):
    def render_screen(self):
        self.render_base()
        for i in range(6):
            pygame.draw.rect(self.av.screen, DARK_GRAY, pygame.Rect(i * self.av.buttonSize, self.av.h - 50, self.av.buttonSize, 50), 2)
        for i in range(5):
            pygame.draw.rect(self.av.screen, DARK_GRAY, pygame.Rect(self.av.buttonSize * 4 + i * self.av.buttonSize / 5, self.av.h - 25, self.av.buttonSize / 5, 25), 2)
        self.render_start_stop()
        self.av.screen.blit(self.av.drawing_state_big_text, [50, self.av.h - 45])
        self.av.screen.blit(self.av.drawing_state_small_text1, [830, self.av.h - 45])
        self.av.screen.blit(self.av.drawing_state_small_text2, [785, self.av.h - 20])
        pygame.display.flip()

    def click(self):
        button_pressed = self.what_is_clicked(pygame.mouse.get_pos())
        if button_pressed == (-1, -1):
            pass
        elif self.av.drawingTool == Tool.WALL:
            self.av.walls.add(button_pressed)
        elif self.av.drawingTool == Tool.START:
            if button_pressed != self.av.end:
                self.av.start = button_pressed
        elif self.av.drawingTool == Tool.END:
            if button_pressed != self.av.start:
                self.av.end = button_pressed
        elif self.av.drawingTool == Tool.ERASER:
            self.av.walls.discard(button_pressed)

    def what_is_clicked(self, mouse_position):
        mouse_x, mouse_y = mouse_position
        if mouse_y < self.av.h - 50:
            return mouse_x // BLOCK_SIZE, mouse_y // BLOCK_SIZE
        else:
            button = mouse_x // self.av.buttonSize + 1
            if button == 1:
                self.av.drawingTool = Tool.WALL
            elif button == 2:
                self.av.drawingTool = Tool.START
            elif button == 3:
                self.av.drawingTool = Tool.END
            elif button == 4:
                self.av.drawingTool = Tool.ERASER
            elif button == 5:
                if mouse_y > self.av.h - 25:
                    percent = ((mouse_x - self.av.buttonSize * 4) // (self.av.buttonSize / 5)) / 10
                    if percent == 0.4:
                        self.av.hard_clear()
                    else:
                        self.generate_maze(percent)
            elif button == 6:
                self.enter()
        return -1, -1

    def enter(self):
        if self.av.start in self.av.walls:
            self.av.walls.discard(self.av.start)
        if self.av.end in self.av.walls:
            self.av.walls.discard(self.av.end)
        self.av.switch_visualization_state()

    def generate_maze(self, percent):
        self.av.start, self.av.end = two_random_even_coord(self.av.x, self.av.y)
        self.av.walls = imperfect_maze_gen(self.av.x, self.av.y, percent)
