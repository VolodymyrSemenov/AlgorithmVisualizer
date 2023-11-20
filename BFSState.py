from State import *
from Algorithms import hsv_to_rgb


class BFSState(WindowState):
    def render_screen(self):
        self.render_animation_base()
        for i in range(1, self.av.maxDepth + 1):
            for coordinate, depth in self.av.depths.items():
                if depth == i:
                    pygame.draw.rect(self.av.screen, hsv_to_rgb(depth, 1, 1, self.av.rainbow_speed_multiplier), pygame.Rect(coordinate[0] * BLOCK_SIZE, coordinate[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(self.av.screen, RED, pygame.Rect(self.av.end[0] * BLOCK_SIZE, self.av.end[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            self.av.clock.tick(10)
            pygame.display.flip()

        self.render_completed_path(50)

        self.av.colorings = self.av.depths
        self.av.switch_visualization_state()
