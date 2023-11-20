from State import *
from Algorithms import hsv_to_rgb


class AStateState(WindowState):
    def render_screen(self):
        self.render_animation_base()

        for tile in self.av.ordered_visited_nodes:
            pygame.draw.rect(self.av.screen, hsv_to_rgb(self.av.depths[tile], 1, 1, self.av.rainbow_speed_multiplier), pygame.Rect(tile[0] * BLOCK_SIZE, tile[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            self.render_start_stop()
            self.av.clock.tick(100)
            pygame.display.flip()

        self.render_completed_path(50)

        self.av.colorings = self.av.depths
        self.av.switch_visualization_state()
