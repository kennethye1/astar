import pygame
from queue import PriorityQueue

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (204, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PEACH = (255, 204, 153)
VIOLET = (153, 153, 255)
LENGTH = 800
WIDTH = 500
pygame.init()
SCREEN = pygame.display.set_mode((LENGTH, WIDTH))

class Cell():
    
    def __init__(self, row, col, size):
        self.row = row
        self.col = col
        self.size = size
        self.color = WHITE
        self.g_cost = self.f_cost = float('inf')
        self.blocked = False
        self.parent = None
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.col*self.size, self.row*self.size, self.size, self.size))
    
    def __lt__(self, other):
        return False


class Grid:
    def __init__(self, length, width, screen, size):
        self.length = length
        self.width = width
        self.screen = screen
        self.size = size
        self.grid = []
        self.rows = self.width // self.size
        self.cols = self.length // self.size 
        
    def draw(self):
        
        for i in range(self.rows):
            self.grid.append([])
            for j in range(self.cols):
                cell = Cell(i, j, self.size)
                cell.draw(self.screen)
                self.grid[i].append(cell)

        pygame.display.update()

    def draw_lines(self):
        for i in range(self.rows):
             pygame.draw.line(self.screen, BLACK, (0, i*self.size), (self.length, i*self.size))
        for j in range(self.cols):
            pygame.draw.line(self.screen, BLACK, (j*self.size, 0), (j*self.size, self.width))
        pygame.display.update()

    def get_neighbors(self, cell):
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i==0) and (j==0):
                    continue
                new_col = i+cell.col
                new_row = j + cell.row
                if (new_col >= 0) and new_col < self.cols and (new_row >= 0) and new_row < self.rows:
                    neighbors.append(self.grid[new_row][new_col])
        return neighbors

def heuristic(start, target):
    #Euclidean distance
    return (start.row-target.row)**2 + (start.col - target.col)**2

def cell_pos(pos, size):
    x, y = pos
    row = y // size
    col = x // size
    return row, col

def get_path(start, screen):
    temp = start
    start.color = VIOLET
    start.draw(screen)
    while temp.parent:
        temp= temp.parent
        if temp.parent:
            temp.color = CYAN
            temp.draw(screen)
    temp.color = PEACH
    temp.draw(screen)

def astar(grid, start, target):
    open_q = PriorityQueue()
    start.g_cost = 0
    start.f_cost = heuristic(start, target)
    open_q.put((0, start.f_cost, start))
    open_set = {start}
    closed = set()
    while not open_q.empty():
        temp = open_q.get()
        curr = temp[2]
        curr.color = RED
        curr.draw(grid.screen)
        closed.add(curr)
        if curr == target:
            get_path(curr, grid.screen)
            return True
        for neighbor in grid.get_neighbors(curr):
            if neighbor.color == BLUE or neighbor in closed:
                continue
            new_cost = curr.g_cost + heuristic(curr, neighbor)
            if new_cost < neighbor.g_cost:
                neighbor.parent = curr
                neighbor.g_cost = new_cost
                neighbor.f_cost = new_cost + heuristic(neighbor, target)
                if neighbor not in open_set:
                    open_set.add(neighbor)
                    open_q.put((neighbor.f_cost, heuristic(neighbor, target), neighbor))
                    neighbor.color = GREEN
                    neighbor.draw(grid.screen)
        pygame.display.update()
                
    return False



def main(screen, length, width, size):
    screen.fill(WHITE)
    running = True
    grid = Grid(length, width, screen, size)
    start = target = None
    grid.draw()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
            
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                i, j = cell_pos(pos, size)
                cell = grid.grid[i][j]
                if not start and cell != target:
                    cell.color = PEACH
                    start = cell
                elif not target and cell != start:
                    cell.color = VIOLET
                    
                    target = cell
                elif cell != target and cell != start:
                    cell.color = BLUE
                    cell.blocked = True
                cell.draw(screen)

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                i, j = cell_pos(pos, size)
                cell = grid.grid[i][j]
                cell.color = WHITE
                cell.draw(screen)
                if cell == start:
                    start = None
                elif cell == target:
                    target = None

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and target:
                    astar(grid, start, target)
        grid.draw_lines()
        pygame.display.update()       
    pygame.quit()

main(SCREEN, LENGTH, WIDTH, 20)
    