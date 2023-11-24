# Colors
BLACK = (0, 0, 0)
EXTRA_DARK_GRAY = (100, 100, 100)
DARK_GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)
WHITE = (255, 255, 255)
ORANGE = (255, 128, 0)
LIGHT_BLUE = (51, 255, 255)
DARK_BLUE = (0, 0, 204)
RED = (255, 0, 0)
PURPLE = (68, 0, 102)
GREEN = (0, 200, 100)

# Sizing/Quantity of grid
BLOCK_SIZE = 20 # Pixels per side of block
X_BLOCKS = 49
Y_BLOCKS = 31

# Random Maze generation
# Percent of blocks to remove for each Random Maze Generation option
RMG_1_REMOVAL = 5
RMG_2_REMOVAL = 15
RMG_3_REMOVAL = 5
RMG_4_REMOVAL = 5
# Higher the number the longer paths will be for random maze generator 3 and 4
RMG_3_LENGTH = 1 # 1+
RMG_4_LENGTH = 7 # 1+

# This determines the weight of the heuristic for A*
# The higher it is, the fewer nodes it will explore at the cost of a worse length path
# At 0 it will behave like BFS
# At 1 it will still find an optimal path
UNOPTIMAL_ASTAR_HEURISTIC_WEIGHT = 2
