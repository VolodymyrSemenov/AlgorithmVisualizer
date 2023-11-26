from enum import Enum

from State import *
from Algorithms import depth_first_search, a_star_search, walls_to_edges, hsv_to_rgb


class Algo(Enum):
    BREADTH_FIRST_SEARCH = 1
    DEPTH_FIRST_SEARCH = 2
    A_STAR_SEARCH = 3
    A_STAR_SEARCH_FAST = 4


class VisualizationState(State):
    selectedAlgo = Algo.BREADTH_FIRST_SEARCH
    fullExplore = False

    def __init__(self, algorithm_visualizer):
        super().__init__(algorithm_visualizer)

    def render_screen(self):
        self.render_base()
        for coordinate, depth in self.av.depths.items():
            pygame.draw.rect(self.av.screen, hsv_to_rgb(depth, 1, 1, self.av.rainbow_speed_multiplier), pygame.Rect(coordinate[0] * BLOCK_SIZE, coordinate[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        for wall in self.av.walls:
            pygame.draw.rect(self.av.screen, BLACK, pygame.Rect(wall[0] * BLOCK_SIZE, wall[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        for i in range(6):
            pygame.draw.rect(self.av.screen, DARK_GRAY, pygame.Rect(i * self.av.buttonSize, self.av.h - 50, self.av.buttonSize, 50), 2)
        for i in range(2):
            pygame.draw.rect(self.av.screen, DARK_GRAY, pygame.Rect(self.av.buttonSize * 2 + i * self.av.buttonSize / 2, self.av.h - 25, self.av.buttonSize / 2, 25), 2)
        for path in self.av.completed_path:
            pygame.draw.rect(self.av.screen, EXTRA_DARK_GRAY, pygame.Rect(path[0] * BLOCK_SIZE, path[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        self.render_start_stop()
        self.render_text()
        pygame.display.flip()


    def render_text(self):
        visualization_state_big_text = self.av.big_font.render("        BFS              DFS                                  Map All            Edit              Next", True, BLACK)
        visualization_state_small_text1 = self.av.small_font.render("                                                                                                                         A*", True, BLACK)
        visualization_state_small_text2 = self.av.small_font.render("                                                                                                         Optimal         Unoptimal", True, BLACK)
        self.av.screen.blit(self.scale_text(visualization_state_big_text), [0, self.av.h - 45])
        self.av.screen.blit(self.scale_text(visualization_state_small_text1), [0, self.av.h - 45])
        self.av.screen.blit(self.scale_text(visualization_state_small_text2), [0, self.av.h - 20])

    def click(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_y < self.av.h - 50:
            return
        button = mouse_x // self.av.buttonSize + 1
        old_selected_algo = self.selectedAlgo
        match button:
            case 1:
                VisualizationState.selectedAlgo = Algo.BREADTH_FIRST_SEARCH
            case 2:
                VisualizationState.selectedAlgo = Algo.DEPTH_FIRST_SEARCH
            case 3:
                if (mouse_x - 2 * self.av.buttonSize) < self.av.buttonSize / 2:
                    VisualizationState.selectedAlgo = Algo.A_STAR_SEARCH
                else:
                    VisualizationState.selectedAlgo = Algo.A_STAR_SEARCH_FAST
            case 4:
                VisualizationState.fullExplore = not self.fullExplore
            case 5:
                self.av.clear_tiles()
                self.av.switch_drawing_state()
            case 6:
                self.enter()
        if self.selectedAlgo != old_selected_algo:
            self.av.clear_tiles()

    def enter(self):
        drawing_edges = walls_to_edges(self.av.walls, self.av.x, self.av.y)
        if self.selectedAlgo == Algo.BREADTH_FIRST_SEARCH:
            self.av.depths, self.av.completed_path, self.av.ordered_visited_nodes = a_star_search(drawing_edges, self.av.start, self.av.end, self.fullExplore, 0)
        elif self.selectedAlgo == Algo.DEPTH_FIRST_SEARCH:
            self.av.depths, self.av.completed_path, self.av.ordered_visited_nodes = depth_first_search(drawing_edges, self.av.start, self.av.end, self.fullExplore)
        elif self.selectedAlgo == Algo.A_STAR_SEARCH:
            self.av.depths, self.av.completed_path, self.av.ordered_visited_nodes = a_star_search(drawing_edges, self.av.start, self.av.end, self.fullExplore, 1)
        elif self.selectedAlgo == Algo.A_STAR_SEARCH_FAST:
            self.av.depths, self.av.completed_path, self.av.ordered_visited_nodes = a_star_search(drawing_edges, self.av.start, self.av.end, self.fullExplore, UNOPTIMAL_ASTAR_HEURISTIC_WEIGHT)

        self.av.maxDepth = max(x for x in self.av.depths.values())
        self.av.rainbow_speed_multiplier = 300 / self.av.maxDepth
        if self.av.rainbow_speed_multiplier < 0.000001:
            self.av.rainbow_speed_multiplier = 1
        self.av.switch_animation_state()
