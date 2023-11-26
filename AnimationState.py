from State import *
from Algorithms import hsv_to_rgb


class AnimationState(State):
    def __init__(self, algorithm_visualizer):
        super().__init__(algorithm_visualizer)
        self.paused = False
        self.counter = 0

    def render_screen(self):
        self.render_base()
        for i in range(2):
            pygame.draw.rect(self.av.screen, DARK_GRAY, pygame.Rect(i * self.av.buttonSize, self.av.h - 50, self.av.buttonSize, 50), 2)
        self.render_text()
        self.counter += max(((self.av.x * self.av.y) - len(self.av.walls)) // 400, 1) if not self.paused else 0
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
    def click(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_y < self.av.h - 50:
            return
        button = mouse_x // self.av.buttonSize + 1
        match button:
            case 1:
                self.enter()
            case 2:
                self.paused = not self.paused

    def enter(self):
        self.av.switch_visualization_state()

    def render_text(self):
        animation_state_big_text = self.av.big_font.render("       Skip             Pause", True, BLACK)
        self.av.screen.blit(self.scale_text(animation_state_big_text), [0, self.av.h - 45])