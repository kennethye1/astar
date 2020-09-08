import pygame
from queue import PriorityQueue
from queue import Queue 

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (204, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PEACH = (255, 204, 153)
VIOLET = (153, 153, 255)
SILVER = (211,211,211)
LENGTH = 1000
WIDTH = 800
BUTTON_WIDTH = 100
pygame.init()
SCREEN = pygame.display.set_mode((LENGTH, WIDTH))
pygame.display.set_caption("Algorithm Visualization")
DELAY_TIME = 80

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
        for i in range(self.rows+1):
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


def bfs(grid, start, target):
    #breadth-first-search
    queue = Queue()
    queue.put(start)
    discovered = {start}
    while not queue.empty():
        delay(DELAY_TIME)
        curr = queue.get()
        if curr != start and curr != target:
            curr.color = RED
            curr.draw(grid.screen)
        if curr == target:
            get_path(curr, grid.screen)
            return True
        for neighbor in grid.get_neighbors(curr):
            if neighbor not in discovered and not neighbor.blocked:
                neighbor.color = GREEN
                neighbor.draw(grid.screen)
                discovered.add(neighbor)
                neighbor.parent = curr
                queue.put(neighbor)
        grid.draw_lines()
    return False

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
        if curr != start and curr != target:
            curr.color = RED 
            curr.draw(grid.screen)
        closed.add(curr)
        delay(DELAY_TIME)
        if curr == target:
            get_path(curr, grid.screen)
            return True
        for neighbor in grid.get_neighbors(curr):
            if neighbor.blocked or neighbor in closed:
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
        grid.draw_lines()
                
    return False

def greedy_bfs(grid, start, target):
    priority = PriorityQueue()
    discovered = {start}
    priority.put((heuristic(start, target), start))
    while not priority.empty():
        delay(DELAY_TIME)
        curr = priority.get()[1]
        if curr != start and curr != target:
            curr.color = RED
            curr.draw(grid.screen)
        if curr == target:
            get_path(curr, grid.screen)
            return True
        for neighbor in grid.get_neighbors(curr):
            if neighbor.blocked or neighbor in discovered:
                continue 
            neighbor.parent = curr
            neighbor.color = GREEN
            neighbor.draw(grid.screen)
            priority.put((heuristic(neighbor, target), neighbor))
            discovered.add(neighbor)
        grid.draw_lines()
    return False

class Button:
    def __init__(self, length, width, color, screen, pos, text):
        self.pos = pos
        self.screen = screen
        self.color = color
        self.length = length
        self.width = width
        self.text = text
        self.rect = pygame.Rect(self.pos, (self.length, self.width))

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        pygame.draw.line(self.screen, BLACK, self.pos, (self.pos[0]+self.length, self.pos[1]))
        pygame.draw.line(self.screen, BLACK, self.pos, (self.pos[0], self.pos[1]+self.width))
        pygame.draw.line(self.screen, BLACK, (self.pos[0]+self.length, self.pos[1]), (self.pos[0]+self.length, self.pos[1]+self.width))
        pygame.draw.line(self.screen, BLACK, (self.pos[0], self.pos[1]+ self.width), (self.pos[0]+self.length, self.pos[1]+self.width))
        font = pygame.font.SysFont('timesnewroman', 15)
        text = font.render(self.text, 1, BLACK)
        self.screen.blit(text, (self.pos[0] + (self.length/2 - text.get_width()/2), self.pos[1] + (self.width/2 - text.get_height()/2)))

def delay(time):
    pygame.time.delay(time)
    pygame.display.update()

def main(screen, length, width, size):
    global DELAY_TIME
    clock = pygame.time.Clock()
    screen.fill(WHITE)
    running = True
    grid = Grid(length, width, screen, size)
    start = target = None
    grid.draw()
    btn_greedy = Button(100, 20, SILVER, screen, (115, 720), "Greedy")
    btn_greedy.draw()
    btn_astar = Button(100, 20, SILVER, screen, (235, 720), "A*-search")
    btn_astar.draw()
    btn_bfs = Button(100, 20, SILVER, screen, (355, 720), "BFS")
    btn_bfs.draw()
    btn_reset = Button(100,20, SILVER, screen, (475, 720), "Reset")
    btn_reset.draw()
    btn_inc = Button(100, 20, SILVER, screen, (595, 720), "Increase Speed")
    btn_inc.draw()
    btn_dec = Button(100, 20, SILVER, screen, (715, 720), "Decrease Speed")
    btn_dec.draw()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
            
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if pos[1] < width:
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
                if start and target:
                    if btn_astar.rect.collidepoint(pos) :
                        astar(grid, start, target)

                    elif btn_greedy.rect.collidepoint(pos):
                        greedy_bfs(grid, start, target)

                    elif btn_reset.rect.collidepoint(pos):
                        start = target = None
                        grid = Grid(length, width, screen, size)
                        grid.draw()    

                    elif btn_bfs.rect.collidepoint(pos):
                        bfs(grid, start, target)
                    
                    elif btn_inc.rect.collidepoint(pos):
                        if DELAY_TIME > 0:
                            DELAY_TIME -= 10
                    elif btn_dec.rect.collidepoint(pos):
                        DELAY_TIME+=10

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                if pos[1] < width:
                    i, j = cell_pos(pos, size)
                    cell = grid.grid[i][j]
                    cell.color = WHITE
                    cell.draw(screen)
                    if cell == start:
                        start = None
                    elif cell == target:
                        target = None
                     
        grid.draw_lines()
        pygame.display.update()
        clock.tick(60)       
    pygame.quit()

main(SCREEN, LENGTH, WIDTH-BUTTON_WIDTH, 20)
    
