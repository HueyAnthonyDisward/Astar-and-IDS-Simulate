import math
import heapq
import pygame


class Cell:
    def __init__(self):
        self.parent_i = 0
        self.parent_j = 0
        self.f = float('inf')
        self.g = float('inf')
        self.h = 0


ROW = 10
COL = 10
WIDTH, HEIGHT = 600, 600
CELL_SIZE = WIDTH // COL


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)


def draw_buttons():
    # Nút A*
    pygame.draw.rect(window, YELLOW, (10, HEIGHT + 10, 100, 40))
    window.blit(font.render("A*", True, BLACK), (30, HEIGHT + 15))

    # Nút IDS
    pygame.draw.rect(window, GREEN, (120, HEIGHT + 10, 100, 40))
    window.blit(font.render("IDS", True, BLACK), (140, HEIGHT + 15))
# Khởi tạo Pygame
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT + 50))  # Thêm khoảng trống cho nút
pygame.display.set_caption("Pathfinding Visualization with IDS")

font = pygame.font.SysFont(None, 36)

# Vẽ lưới
def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        for y in range(0, HEIGHT, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(window, BLACK, rect, 1)

# Vẽ từng bước đi trên lưới
def draw_step(grid, path, step_index, src, dest):
    window.fill(WHITE)
    for row in range(ROW):
        for col in range(COL):
            color = WHITE if grid[row][col] == 0 else BLACK
            pygame.draw.rect(window, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Tô màu điểm bắt đầu và kết thúc
    pygame.draw.rect(window, YELLOW, (src[1] * CELL_SIZE, src[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(window, RED, (dest[1] * CELL_SIZE, dest[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Tô màu các bước đã đi qua
    for (row, col) in path[:step_index + 1]:
        pygame.draw.rect(window, BLUE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    draw_grid()
    draw_buttons()
    pygame.display.update()

# Kiểm tra tính hợp lệ của ô
def is_valid(row, col):
    return (row >= 0) and (row < ROW) and (col >= 0) and (col < COL)

# Kiểm tra xem ô có phải là ô có thể đi được
def is_unblocked(grid, row, col):
    return grid[row][col] == 0

# Kiểm tra xem ô có phải là đích
def is_destination(row, col, dest):
    return row == dest[0] and col == dest[1]

# Tính toán giá trị heuristic
def calculate_h_value(row, col, dest):
    return ((row - dest[0]) ** 2 + (col - dest[1]) ** 2) ** 0.5

# Tìm đường đi từ nguồn đến đích
def trace_path(cell_details, dest):
    """ Truy vết đường đi từ ô đích về nguồn. """
    path = []
    row, col = dest
    while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
        path.append((row, col))
        temp_row = cell_details[row][col].parent_i
        temp_col = cell_details[row][col].parent_j
        row, col = temp_row, temp_col
    path.append((row, col))  # Thêm ô nguồn vào đường đi
    path.reverse()  # Đảo ngược để có đường đi từ nguồn đến đích
    return path

# Thuật toán A* tìm đường đi từ nguồn đến đích
def a_star_search(grid, src, dest):
    """ Thực hiện thuật toán A* để tìm đường đi tối ưu. """
    if not is_valid(src[0], src[1]) or not is_valid(dest[0], dest[1]):
        print("Nguồn hoặc đích không hợp lệ")
        return None

    if not is_unblocked(grid, src[0], src[1]) or not is_unblocked(grid, dest[0], dest[1]):
        print("Nguồn hoặc đích bị chặn")
        return None

    if is_destination(src[0], src[1], dest):
        print("Đã ở đích")
        return [src]

    # Khởi tạo danh sách đã đóng và chi tiết ô
    closed_list = [[False for _ in range(COL)] for _ in range(ROW)]
    cell_details = [[Cell() for _ in range(COL)] for _ in range(ROW)]

    i, j = src
    cell_details[i][j].f = cell_details[i][j].g = cell_details[i][j].h = 0
    cell_details[i][j].parent_i = i
    cell_details[i][j].parent_j = j

    open_list = []  # Danh sách mở để theo dõi các ô sẽ kiểm tra
    heapq.heappush(open_list, (0.0, i, j))  # Thêm ô nguồn vào danh sách mở
    found_dest = False

    while len(open_list) > 0:
        # Lấy ô có f nhỏ nhất từ danh sách mở
        p = heapq.heappop(open_list)
        i, j = p[1], p[2]
        closed_list[i][j] = True  # Đánh dấu ô là đã kiểm tra

        # Duyệt qua các hướng di chuyển
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dir in directions:
            new_i, new_j = i + dir[0], j + dir[1]

            # Kiểm tra xem ô mới có hợp lệ không
            if is_valid(new_i, new_j) and is_unblocked(grid, new_i, new_j) and not closed_list[new_i][new_j]:
                if is_destination(new_i, new_j, dest):
                    cell_details[new_i][new_j].parent_i = i
                    cell_details[new_i][new_j].parent_j = j
                    return trace_path(cell_details, dest)  # Truy vết đường đi đến đích
                else:
                    g_new = cell_details[i][j].g + 1.0  # Chi phí từ nguồn đến ô mới
                    h_new = calculate_h_value(new_i, new_j, dest)  # Tính toán h
                    f_new = g_new + h_new  # Tính toán f

                    # Nếu ô mới có f nhỏ hơn, cập nhật chi tiết ô
                    if cell_details[new_i][new_j].f == float('inf') or cell_details[new_i][new_j].f > f_new:
                        heapq.heappush(open_list, (f_new, new_i, new_j))  # Thêm ô mới vào danh sách mở
                        cell_details[new_i][new_j].f = f_new
                        cell_details[new_i][new_j].g = g_new
                        cell_details[new_i][new_j].h = h_new
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j

    return None  # Trả về None nếu không tìm thấy đường đi

# Hàm tìm kiếm IDS
def ids_search(grid, src, dest):
    """ Tìm đường đi bằng thuật toán IDS. """
    def dfs_limit(row, col, depth, visited, cell_details):
        if depth == 0:
            return None
        visited.add((row, col))  # Đánh dấu ô hiện tại là đã duyệt

        if is_destination(row, col, dest):
            return trace_path(cell_details, dest)

        # Duyệt qua các hướng di chuyển
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for d in directions:
            new_i, new_j = row + d[0], col + d[1]
            if is_valid(new_i, new_j) and is_unblocked(grid, new_i, new_j) and (new_i, new_j) not in visited:
                cell_details[new_i][new_j].parent_i = row
                cell_details[new_i][new_j].parent_j = col
                result = dfs_limit(new_i, new_j, depth - 1, visited, cell_details)
                if result is not None:
                    return result

        visited.remove((row, col))  # Khôi phục trạng thái để cho phép duyệt lại
        return None

    for depth in range(1, ROW * COL + 1):
        visited = set()  # Sử dụng tập hợp để theo dõi các ô đã được duyệt
        cell_details = [[Cell() for _ in range(COL)] for _ in range(ROW)]
        i, j = src
        cell_details[i][j].parent_i = i
        cell_details[i][j].parent_j = j
        path = dfs_limit(i, j, depth, visited, cell_details)
        if path:
            return path  # Trả về đường đi nếu tìm thấy

    return None  # Trả về None nếu không tìm thấy đường đi

# Hàm chính
def main():
        grid = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        ]

        src = [0, 0]
        dest = [8, 9]
        step_index = 0
        running = True
        path_found = False
        path_ids = False
        path = None

        # Khởi tạo và vẽ bảng lưới
        window.fill(WHITE)
        draw_step(grid, [], -1, src, dest)

        # Vẽ các nút điều khiển
        pygame.draw.rect(window, YELLOW, (10, HEIGHT + 10, 100, 40))
        window.blit(font.render("A*", True, BLACK), (30, HEIGHT + 15))

        pygame.draw.rect(window, GREEN, (120, HEIGHT + 10, 100, 40))
        window.blit(font.render("IDS", True, BLACK), (140, HEIGHT + 15))

        # Vẽ lại lưới để không bị che khuất
        draw_grid()
        pygame.display.update()

        # Vòng lặp sự kiện Pygame
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    # Xử lý nút A*
                    if 10 <= mouse_x <= 110 and HEIGHT + 10 <= mouse_y <= HEIGHT + 50:
                        path = a_star_search(grid, src, dest)
                        path_found = True
                        step_index = 0
                    # Xử lý nút IDS
                    elif 120 <= mouse_x <= 220 and HEIGHT + 10 <= mouse_y <= HEIGHT + 50:
                        path = ids_search(grid, src, dest)
                        path_ids = True
                        step_index = 0

            # Chỉ vẽ từng bước nếu đường đi đã được tìm thấy
            if path_found or path_ids:
                if step_index < len(path):
                    draw_step(grid, path, step_index, src, dest)
                    pygame.time.wait(500)  # 0.5 giây mỗi bước
                    step_index += 1
                else:
                    path_found = False
                    path_ids = False

            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    main()

#Link em tham khảo trên:  https://www.geeksforgeeks.org/a-search-algorithm/ + https://www.geeksforgeeks.org/iterative-deepening-searchids-iterative-deepening-depth-first-searchiddfs/