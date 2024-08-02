import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 400, 500
GRID_SIZE = 4
TILE_SIZE = WIDTH // GRID_SIZE
FONT = pygame.font.Font(None, 36)
SCORE_FONT = pygame.font.Font(None, 48)

# Colors
BACKGROUND_COLOR = (251, 248, 241)  # Light cream background
EMPTY_TILE_COLOR = (205, 193, 180)  # Light gray for empty tiles
TILE_COLORS = {
    2: (255, 255, 63),    # #FFFF3F
    4: (158, 240, 26),    # #9EF01A
    8: (82, 183, 136),    # #52B788
    16: (157, 217, 210),  # #9DD9D2
    32: (66, 191, 221),   # #42BFDD
    64: (98, 182, 203),   # #62B6CB
    128: (242, 177, 121),
    256: (245, 149, 99),
    512: (246, 124, 95),
    1024: (237, 207, 114),
    2048: (237, 194, 46)
}

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")

class Game2048:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4

    def move(self, direction):
        moved = False
        if direction == "up":
            for j in range(GRID_SIZE):
                column = [self.grid[i][j] for i in range(GRID_SIZE) if self.grid[i][j] != 0]
                column, score = self.merge(column)
                self.score += score
                for i in range(GRID_SIZE):
                    value = column[i] if i < len(column) else 0
                    if self.grid[i][j] != value:
                        moved = True
                    self.grid[i][j] = value
        elif direction == "down":
            for j in range(GRID_SIZE):
                column = [self.grid[i][j] for i in range(GRID_SIZE-1, -1, -1) if self.grid[i][j] != 0]
                column, score = self.merge(column)
                self.score += score
                for i in range(GRID_SIZE-1, -1, -1):
                    value = column[GRID_SIZE-1-i] if GRID_SIZE-1-i < len(column) else 0
                    if self.grid[i][j] != value:
                        moved = True
                    self.grid[i][j] = value
        elif direction == "left":
            for i in range(GRID_SIZE):
                row = [self.grid[i][j] for j in range(GRID_SIZE) if self.grid[i][j] != 0]
                row, score = self.merge(row)
                self.score += score
                for j in range(GRID_SIZE):
                    value = row[j] if j < len(row) else 0
                    if self.grid[i][j] != value:
                        moved = True
                    self.grid[i][j] = value
        elif direction == "right":
            for i in range(GRID_SIZE):
                row = [self.grid[i][j] for j in range(GRID_SIZE-1, -1, -1) if self.grid[i][j] != 0]
                row, score = self.merge(row)
                self.score += score
                for j in range(GRID_SIZE-1, -1, -1):
                    value = row[GRID_SIZE-1-j] if GRID_SIZE-1-j < len(row) else 0
                    if self.grid[i][j] != value:
                        moved = True
                    self.grid[i][j] = value
        if moved:
            self.add_new_tile()
        return moved

    def merge(self, line):
        score = 0
        for i in range(len(line) - 1):
            if line[i] == line[i + 1]:
                line[i] *= 2
                score += line[i]
                line[i + 1] = 0
        return [tile for tile in line if tile != 0], score

    def draw(self):
        screen.fill(BACKGROUND_COLOR)
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = self.grid[i][j]
                color = TILE_COLORS.get(value, EMPTY_TILE_COLOR)
                pygame.draw.rect(screen, color, (j*TILE_SIZE+5, i*TILE_SIZE+5, TILE_SIZE-10, TILE_SIZE-10), border_radius=8)
                if value != 0:
                    text_color = (0, 0, 0) if value <= 4 else (255, 255, 255)
                    text_surface = FONT.render(str(value), True, text_color)
                    text_rect = text_surface.get_rect(center=(j*TILE_SIZE + TILE_SIZE//2, i*TILE_SIZE + TILE_SIZE//2))
                    screen.blit(text_surface, text_rect)

        # Draw score
        score_text = SCORE_FONT.render(f"Score: {self.score}", True, (0, 0, 0))
        screen.blit(score_text, (10, HEIGHT - 60))

    def game_over(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.grid[i][j] == 0:
                    return False
                if i < GRID_SIZE - 1 and self.grid[i][j] == self.grid[i][j + 1]:
                    return False
                if j < GRID_SIZE - 1 and self.grid[i][j] == self.grid[i + 1][j]:
                    return False
        return True

def main():
    game = Game2048()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.move("up")
                elif event.key == pygame.K_DOWN:
                    game.move("down")
                elif event.key == pygame.K_LEFT:
                    game.move("left")
                elif event.key == pygame.K_RIGHT:
                    game.move("right")

        game.draw()
        pygame.display.flip()

        if game.game_over():
            font = pygame.font.Font(None, 74)
            text = font.render("Game Over", True, (255, 0, 0))
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()