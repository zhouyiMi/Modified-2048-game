import pygame  
import random  
import sys  

# 游戏参数  
WIDTH, HEIGHT = 400, 400  
GRID_SIZE = 4  
GRID_PADDING = 10  
BACKGROUND_COLOR = (187, 173, 160)  
CELL_COLORS = {  
    0: (205, 193, 180),  
    2: (238, 228, 218),  
    4: (237, 224, 200),  
    8: (242, 177, 121),  
    16: (245, 149, 99),  
    32: (246, 124, 95),  
    64: (246, 94, 59),  
    128: (237, 207, 114),  
    256: (237, 204, 97),  
    512: (237, 200, 80),  
    1024: (237, 197, 63),  
    2048: (237, 194, 46),  
}  

# 初始化游戏  
pygame.init()  
screen = pygame.display.set_mode((WIDTH, HEIGHT))  
pygame.display.set_caption('2048')  

# 创建空白网格  
def create_grid():  
    return [[0] * GRID_SIZE for _ in range(GRID_SIZE)]  

# 在第一行随机生成一个新数字  
def spawn_number(grid):  
    if grid[0].count(0) > 0:  # 检查第一行是否有空位  
        c = random.randint(0, GRID_SIZE - 1)  
        grid[0][c] = random.choice([2, 4])  

# 显示网格  
def draw_grid(grid):  
    for r in range(GRID_SIZE):  
        for c in range(GRID_SIZE):  
            value = grid[r][c]  
            pygame.draw.rect(screen, CELL_COLORS[value],   
                             (c * 100 + GRID_PADDING, r * 100 + GRID_PADDING, 100 - GRID_PADDING, 100 - GRID_PADDING))  
            if value != 0:  
                font = pygame.font.Font(None, 55)  
                text = font.render(str(value), True, (0, 0, 0))  
                text_rect = text.get_rect(center=(c * 100 + 50, r * 100 + 50))  
                screen.blit(text, text_rect)  

# 将数字向左移动并合并  
def move_left(grid):  
    for r in range(GRID_SIZE):  
        new_row = [num for num in grid[r] if num != 0]  # 移除零  
        merged_row = []  
        skip = False  
        
        for i in range(len(new_row)):  
            if skip:  
                skip = False  
                continue  
            # 合并相同的数字  
            if i + 1 < len(new_row) and new_row[i] == new_row[i + 1]:  
                merged_row.append(new_row[i] * 2)  
                skip = True  # 跳过下一个数字  
            else:  
                merged_row.append(new_row[i])  
        
        # 填充行的剩余部分为0  
        while len(merged_row) < GRID_SIZE:  
            merged_row.append(0)  
        
        grid[r] = merged_row  

# 向下移动  
def move_down(grid):  
    grid = rotate_grid(grid)  
    move_left(grid)  
    grid = rotate_grid(grid, -1)  
    return grid  

# 逆时针旋转网格  
def rotate_grid(grid, times=1):  
    for _ in range(times % 4):  
        grid = [list(reversed(col)) for col in zip(*grid)]  
    return grid  

# 检查游戏是否结束  
def is_game_over(grid):  
    for r in range(GRID_SIZE):  
        for c in range(GRID_SIZE):  
            if grid[r][c] == 0:  
                return False  
            if c < GRID_SIZE - 1 and grid[r][c] == grid[r][c + 1]:  
                return False  
            if r < GRID_SIZE - 1 and grid[r][c] == grid[r + 1][c]:  
                return False  
    return True  

# 主循环  
def main():  
    grid = create_grid()  
    spawn_number(grid)  # 初始时添加一个数字  
    spawn_number(grid)  # 初始时再添加一个数字  

    while True:  
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                pygame.quit()  
                sys.exit()  
            if event.type == pygame.KEYDOWN:  
                if event.key == pygame.K_LEFT:  
                    move_left(grid)  
                elif event.key == pygame.K_DOWN:  
                    grid = move_down(grid)  
                elif event.key == pygame.K_RIGHT:  
                    grid = rotate_grid(grid, 2)  # 向右移动 = 先旋转180度，然后向左移动  
                    move_left(grid)  
                    grid = rotate_grid(grid, -2)  
                
                spawn_number(grid)  # 每次移动后生成新数字  

        screen.fill(BACKGROUND_COLOR)  
        draw_grid(grid)  

        if is_game_over(grid):  
            font = pygame.font.Font(None, 55)  
            game_over_text = font.render('Game Over!', True, (255, 0, 0))  
            screen.blit(game_over_text, (WIDTH // 4, HEIGHT // 2 - 30))  
            restart_text = font.render('Press R to Restart', True, (0, 0, 0))  
            screen.blit(restart_text, (WIDTH // 6, HEIGHT // 2 + 20))  
            pygame.display.flip()  
            waiting = True  
            while waiting:  
                for event in pygame.event.get():  
                    if event.type == pygame.KEYDOWN:  
                        if event.key == pygame.K_r:  
                            main()  # 重新开始游戏  
                        if event.type == pygame.QUIT:  
                            pygame.quit()  
                            sys.exit()  

        pygame.display.flip()  

if __name__ == "__main__":  
    main()