import pygame

WIDTH = 800
FPS = 10
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Conway's Game of Life")

GREY = (128, 128, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Cell:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.colour = WHITE
        self.neighbors = []
        self.living_neighbors = 0
        self.width = width
        self.total_rows = total_rows
    def get_pos(self):
        return self.row, self.col
    def is_alive(self):
        return self.colour == BLACK
    def is_born(self):
        return self.colour == GREEN
    def is_dying(self):
        return self.colour == RED
    def is_dead(self):
        return self.colour == WHITE
    def make_dead(self):
        self.colour = WHITE
    def make_alive(self):
        self.colour = BLACK
    def make_born(self):
        self.colour = GREEN
    def make_dying(self):
        self.colour = RED
    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.width))
    def update_cell(self, grid):
        self.neighbors = []
        self.living_neighbors = 0
        if self.row < self.total_rows - 1:
            self.neighbors.append(grid[self.row + 1][self.col]) #DOWN
            if self.col < self.total_rows - 1:
                self.neighbors.append(grid[self.row + 1][self.col + 1]) #DOWN RIGHT
            if self.col > 0:
                self.neighbors.append(grid[self.row + 1][self.col - 1]) #DOWN LEFT
        if self.row > 0:
            self.neighbors.append(grid[self.row - 1][self.col]) #UP
            if self.col < self.total_rows - 1:
                self.neighbors.append(grid[self.row - 1][self.col + 1]) #UP RIGHT
            if self.col > 0:
                self.neighbors.append(grid[self.row - 1][self.col - 1]) #UP LEFT
        if self.col < self.total_rows - 1:
            self.neighbors.append(grid[self.row][self.col + 1]) #RIGHT
        if self.col > 0:
            self.neighbors.append(grid[self.row][self.col - 1]) #LEFT
        for cell in self.neighbors:
            if cell.is_alive() or cell.is_dying():
                self.living_neighbors += 1
        if self.is_dead() and self.living_neighbors == 3:
            self.make_born()
        if self.is_alive() and (self.living_neighbors < 2 or self.living_neighbors > 3):
            self.make_dying()
    def next_tick(self):
        if self.is_dying():
            self.make_dead()
        if self.is_born():
            self.make_alive()


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            cell = Cell(i, j, gap, rows)
            grid[i].append(cell)
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for cell in row:
            cell.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col

def main(win, width):
    ROWS = 50
    clock = pygame.time.Clock()
    grid = make_grid(ROWS, width)
    run = True
    started = False
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]: #LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                cell = grid[row][col]
                cell.make_alive()
            elif pygame.mouse.get_pressed()[2]: #RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                cell = grid[row][col]
                cell.make_dead()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    started = True
                    while started:
                        clock.tick(FPS)
                        draw(win, grid, ROWS, width)
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                started = False
                                run = False
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE:
                                    started = False
                        for row in grid:
                            for cell in row:
                                cell.update_cell(grid)
                        #draw(win, grid, ROWS, width) # uncommenting this line will draw the dying and born steps for each cell
                        for row in grid:
                            for cell in row:
                                cell.next_tick()
    pygame.quit()
main(WIN, WIDTH)