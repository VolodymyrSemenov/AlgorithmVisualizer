from State import *
from Algorithms import hsv_to_rgb


class AnimationState(State):
    def __init__(self, algorithm_visualizer):
        super().__init__(algorithm_visualizer)
        self.counter = 0

    def render_screen(self):
        self.render_base()
        self.counter += max(((self.av.x * self.av.y) - len(self.av.walls)) // 200, 1)
        for tile in self.av.ordered_visited_nodes[0:self.counter]:
            pygame.draw.rect(self.av.screen, hsv_to_rgb(self.av.depths[tile], 1, 1, self.av.rainbow_speed_multiplier), pygame.Rect(tile[0] * BLOCK_SIZE, tile[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        self.render_start_stop()
        if self.counter < len(self.av.ordered_visited_nodes):
            pygame.display.flip()
            return

        for path in self.av.completed_path[0:self.counter - len(self.av.ordered_visited_nodes)]:
            pygame.draw.rect(self.av.screen, EXTRA_DARK_GRAY, pygame.Rect(path[0] * BLOCK_SIZE, path[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        if self.counter < len(self.av.ordered_visited_nodes) + len(self.av.completed_path):
            pygame.display.flip()
            return

        self.av.switch_visualization_state()

    def enter(self):
        self.av.switch_visualization_state()

