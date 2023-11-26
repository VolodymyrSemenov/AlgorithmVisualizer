from enum import Enum
import random

import pygame

from Algorithms import prims_maze_gen, kruskals_maze_gen, two_random_coord
from State import State
from Constants import *


class Tool(Enum):
    WALL = 1
    START = 2
    END = 3
    ERASER = 4


class DrawingState(State):
    def __init__(self, algorithm_visualizer):
        super().__init__(algorithm_visualizer)
        self.drawingTool = Tool.WALL

    def render_screen(self):
        self.render_base()
        for i in range(6):
            pygame.draw.rect(self.av.screen, DARK_GRAY, pygame.Rect(i * self.av.buttonSize, self.av.h - 50, self.av.buttonSize, 50), 2)
        for i in range(5):
            pygame.draw.rect(self.av.screen, DARK_GRAY, pygame.Rect(self.av.buttonSize * 4 + i * self.av.buttonSize / 5, self.av.h - 25, self.av.buttonSize / 5, 25), 2)
        pygame.draw.rect(self.av.screen, BLACK, pygame.Rect((self.drawingTool.value-1) * self.av.buttonSize, self.av.h - 50, self.av.buttonSize, 50), 2)

        self.render_start_stop()
        self.render_text()
        pygame.display.flip()

    def render_text(self):
        drawing_state_big_text = self.av.big_font.render("      Walls               Start              End              Erase                                    Next", True, BLACK)
        drawing_state_small_text1 = self.av.small_font.render("                                                                                                                                                                                                              GENERATE MAZE", True, BLACK)
        drawing_state_small_text2 = self.av.small_font.render("                                                                                                                                                                                                        1        2        3       4     CLR", True, BLACK)

        self.av.screen.blit(self.scale_text(drawing_state_big_text), [0, self.av.h - 45])
        self.av.screen.blit(self.scale_text(drawing_state_small_text1), [0, self.av.h - 45])
        self.av.screen.blit(self.scale_text(drawing_state_small_text2), [0, self.av.h - 20])

    def click(self):
        block_pressed = self.block_pressed(pygame.mouse.get_pos())
        match block_pressed:
            case None:
                pass
            case Tool.WALL:
                self.av.walls.add(block_pressed)
            case Tool.START:
                if block_pressed != self.av.end:
                    self.av.start = block_pressed
            case Tool.END:
                if block_pressed != self.av.start:
                    self.av.end = block_pressed
            case Tool.ERASER:
                self.av.walls.discard(block_pressed)

    def block_pressed(self, mouse_position):
        mouse_x, mouse_y = mouse_position
        if mouse_y < self.av.h - 50:
            return mouse_x // BLOCK_SIZE, mouse_y // BLOCK_SIZE
        button_clicked =  mouse_x // self.av.buttonSize + 1
        match button_clicked:
            case 1:
                self.drawingTool = Tool.WALL
            case 2:
                self.drawingTool = Tool.START
            case 3:
                self.drawingTool = Tool.END
            case 4:
                self.drawingTool = Tool.ERASER
            case 5:
                if mouse_y > self.av.h - 25:
                    small_block = (mouse_x - self.av.buttonSize * 4) // (self.av.buttonSize / 5) + 1
                    match small_block:
                        case 1:
                            self.av.walls = kruskals_maze_gen(self.av.x, self.av.y)
                            self.delete_walls(RMG_1_REMOVAL)
                            self.randomize_start_stop()
                        case 2:
                            self.av.walls = kruskals_maze_gen(self.av.x, self.av.y)
                            self.delete_walls(RMG_2_REMOVAL)
                            self.randomize_start_stop()
                        case 3:
                            self.av.walls = prims_maze_gen(self.av.x, self.av.y, RMG_3_LENGTH)
                            self.delete_walls(RMG_3_REMOVAL)
                            self.randomize_start_stop()
                        case 4:
                            self.av.walls = prims_maze_gen(self.av.x, self.av.y, RMG_4_LENGTH)
                            self.delete_walls(RMG_4_REMOVAL)
                            self.randomize_start_stop()
                        case 5:
                            self.av.hard_clear()
            case 6:
                self.enter()
        return

    def enter(self):
        if self.av.start in self.av.walls:
            self.av.walls.discard(self.av.start)
        if self.av.end in self.av.walls:
            self.av.walls.discard(self.av.end)
        self.av.switch_visualization_state()

    def randomize_start_stop(self):
        self.av.start, self.av.end = two_random_coord(self.av.x, self.av.y)
        while self.av.start in self.av.walls or self.av.end in self.av.walls:
            self.av.start, self.av.end = two_random_coord(self.av.x, self.av.y)

    def delete_walls(self, percent_to_remove):
        walls = list(self.av.walls)
        random.shuffle(walls)
        self.av.walls = set(walls[len(walls) * percent_to_remove // 100:])