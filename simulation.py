import sys
import pygame
from collections import deque
import heapq

# =============== TEMEL AYARLAR ===============

UI_HEIGHT = 60   # üstte yazı alanı
CELL_SIZE = 40   # kare boyutu


# 0 = yol, 1 = engel, S = başlangıç, G = hedef, T = trafik lambası
BASE_GRID = [
    ['S', 0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
    [0,   1,   1,   0,   1,   0,   1,   0,   1,   0,   1,   0,   1,   0,   0],
    [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   0,   0],
    [1,   1,   0,   1,   1,   1,   0,   1,   1,   1,   0,   1,   1,   1,   0],
    [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
    [0,   1,   1,   1,   1,   1,   0,   1,   1,   1,   0,   1,   1,   1,   0],
    [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
    [0,   1,   1,   1,   0,   1,   1,   1,   0,   1,   1,   1,   0,   1,   0],
    [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
    [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  'G'],
]

ROWS = len(BASE_GRID)
COLS = len(BASE_GRID[0])


class TrafficLight:
    def __init__(self, position=None, red_time=3, green_time=3):
        self.position = position
        self.red_time = red_time
        self.green_time = green_time
        self.time = 0

    def is_red(self):
        cycle = self.red_time + self.green_time
        t = self.time % cycle
        return t < self.red_time

    def update(self):
        self.time += 1


# =============== YARDIMCI FONKSİYONLAR ===============

def copy_grid():
    return [row[:] for row in BASE_GRID]


def find_start_goal(g):
    start = None
    goal = None
    for r in range(len(g)):
        for c in range(len(g[0])):
            if g[r][c] == 'S':
                start = (r, c)
            elif g[r][c] == 'G':
                goal = (r, c)
    return start, goal


def find_traffic_light_pos(g):
    for r in range(len(g)):
        for c in range(len(g[0])):
            if g[r][c] == 'T':
                return (r, c)
    return None


def is_free(g, r, c):
    if r < 0 or c < 0 or r >= len(g) or c >= len(g[0]):
        return False
    cell = g[r][c]
    if cell == 0 or cell == 'S' or cell == 'G' or cell == 'T':
        return True
    else:
        return False


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# =============== ALGORİTMALAR ===============

def bfs(g, start, goal):
    queue = deque([start])
    visited = {start: None}
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        current = queue.popleft()
        if current == goal:
            break

        r, c = current
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            neighbour = (nr, nc)

            if is_free(g, nr, nc) and neighbour not in visited:
                visited[neighbour] = current
                queue.append(neighbour)

    if goal not in visited:
        return []

    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = visited[cur]
    path.reverse()
    return path


def greedy_path(g, start, goal, max_steps=1000):
    current = start
    path = [current]
    visited = {current}
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for _ in range(max_steps):
        if current == goal:
            break

        r, c = current
        best_neighbour = None
        best_h = float('inf')

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            neighbour = (nr, nc)

            if not is_free(g, nr, nc) or neighbour in visited:
                continue

            h = manhattan(neighbour, goal)
            if h < best_h:
                best_h = h
                best_neighbour = neighbour

        if best_neighbour is None:
            break

        current = best_neighbour
        path.append(current)
        visited.add(current)

    if path[-1] != goal:
        print("Greedy hedefe ulaşamadı veya takıldı.")
    return path


def astar_path(g, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {start: None}
    g_score = {start: 0}
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            break

        r, c = current
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            neighbour = (nr, nc)

            if not is_free(g, nr, nc):
                continue

            tentative_g = g_score[current] + 1

            if neighbour not in g_score or tentative_g < g_score[neighbour]:
                g_score[neighbour] = tentative_g
                f_score = tentative_g + manhattan(neighbour, goal)
                heapq.heappush(open_set, (f_score, neighbour))
                came_from[neighbour] = current

    if goal not in came_from:
        return []

    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = came_from[cur]
    path.reverse()
    return path


def compute_path(algo_name, g, start, goal):
    if not start or not goal:
        return []
    if algo_name == "BFS":
        return bfs(g, start, goal)
    elif algo_name == "Greedy":
        return greedy_path(g, start, goal)
    elif algo_name == "A*":
        return astar_path(g, start, goal)
    else:
        return []


# =============== PYGAME BAŞLANGIÇ ===============

pygame.init()
grid = copy_grid()
start, goal = find_start_goal(grid)
traffic_light = TrafficLight(find_traffic_light_pos(grid), red_time=3, green_time=3)

current_algo = "BFS"
edit_mode = "none"   # "obstacle", "start", "goal", "traffic"

path = compute_path(current_algo, grid, start, goal)
path_index = 0

WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE + UI_HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Otonom Araç Simülasyonu - 1:BFS 2:Greedy 3:A* | O/S/G/T düzenleme")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)


def recalc_everything():
    """Grid değiştiğinde S, G, trafik ışığı ve yolu güncelle."""
    global start, goal, path, path_index
    start, goal = find_start_goal(grid)
    tl_pos = find_traffic_light_pos(grid)
    traffic_light.position = tl_pos
    path = compute_path(current_algo, grid, start, goal)
    path_index = 0


def set_single_cell(char, r, c):
    """S, G veya T taşırken eskiyi sil, yeniyi koy."""
    # Eskiyi sil
    for rr in range(ROWS):
        for cc in range(COLS):
            if grid[rr][cc] == char:
                grid[rr][cc] = 0
    # Yeniyi koy
    grid[r][c] = char


running = True
while running:
    clock.tick(5)  # biraz akıcı hız

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Algoritma seçimi
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_algo = "BFS"
                recalc_everything()
            elif event.key == pygame.K_2:
                current_algo = "Greedy"
                recalc_everything()
            elif event.key == pygame.K_3:
                current_algo = "A*"
                recalc_everything()

            # Düzenleme modları
            elif event.key == pygame.K_o:
                edit_mode = "obstacle"
            elif event.key == pygame.K_s:
                edit_mode = "start"
            elif event.key == pygame.K_g:
                edit_mode = "goal"
            elif event.key == pygame.K_t:
                edit_mode = "traffic"
            elif event.key == pygame.K_r:
                # haritayı tamamen sıfırla
                grid = copy_grid()
                start, goal = find_start_goal(grid)
                traffic_light.position = find_traffic_light_pos(grid)
                path = compute_path(current_algo, grid, start, goal)
                path_index = 0
                edit_mode = "none"

        # Fare ile tıklama
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            if my >= UI_HEIGHT:
                c = mx // CELL_SIZE
                r = (my - UI_HEIGHT) // CELL_SIZE
                if 0 <= r < ROWS and 0 <= c < COLS:
                    cell = grid[r][c]

                    if edit_mode == "obstacle":
                        # sadece yol/engel arasında değiştir
                        if cell == 0:
                            grid[r][c] = 1
                        elif cell == 1:
                            grid[r][c] = 0
                    elif edit_mode == "start":
                        set_single_cell('S', r, c)
                    elif edit_mode == "goal":
                        set_single_cell('G', r, c)
                    elif edit_mode == "traffic":
                        # aynı yere basılırsa kaldır
                        if cell == 'T':
                            grid[r][c] = 0
                            traffic_light.position = None
                        else:
                            set_single_cell('T', r, c)

                    recalc_everything()

    # --- Yol ve trafik ışığı güncelleme ---
    if path:
        current_cell = path[path_index]

        # Trafik ışığı varsa ve kırmızıysa bekle
        if (
            traffic_light.position is not None
            and current_cell == traffic_light.position
            and traffic_light.is_red()
        ):
            pass
        else:
            if path_index < len(path) - 1:
                path_index += 1
                current_cell = path[path_index]

    traffic_light.update()

    # --- ÇİZİM ---
    screen.fill((20, 20, 30))

    # Harita
    for r in range(ROWS):
        for c in range(COLS):
            cell = grid[r][c]
            rect = pygame.Rect(
                c * CELL_SIZE,
                UI_HEIGHT + r * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )

            if cell == 1:
                color = (80, 80, 80)          # engel
            elif cell == 'S':
                color = (0, 90, 220)          # başlangıç
            elif cell == 'G':
                color = (0, 190, 0)           # hedef
            elif cell == 'T':
                if traffic_light.is_red():
                    color = (230, 40, 40)     # kırmızı ışık
                else:
                    color = (60, 210, 60)     # yeşil ışık
            else:
                color = (45, 45, 55)          # normal yol

            pygame.draw.rect(screen, color, rect, border_radius=6)
            pygame.draw.rect(screen, (90, 90, 100), rect, 1)

    # Yolu çizgi ile göster
    if len(path) > 1:
        points = []
        for (pr, pc) in path:
            x = pc * CELL_SIZE + CELL_SIZE // 2
            y = UI_HEIGHT + pr * CELL_SIZE + CELL_SIZE // 2
            points.append((x, y))
        pygame.draw.lines(screen, (0, 150, 255), False, points, 3)

    # Aracı çiz
    if path:
        car_r, car_c = path[path_index]
    elif start:
        car_r, car_c = start
    else:
        car_r, car_c = 0, 0

    car_x = car_c * CELL_SIZE + CELL_SIZE // 2
    car_y = UI_HEIGHT + car_r * CELL_SIZE + CELL_SIZE // 2
    pygame.draw.circle(screen, (255, 230, 0), (car_x, car_y), CELL_SIZE // 2 - 4)

    # Üst yazılar
    mode_text_map = {
        "none": "Düzenleme modu: yok",
        "obstacle": "Düzenleme modu: Engel (O)",
        "start": "Düzenleme modu: Başlangıç (S)",
        "goal": "Düzenleme modu: Hedef (G)",
        "traffic": "Düzenleme modu: Trafik lambası (T)",
    }
    text1 = font.render(
        f"Algoritma: {current_algo}  (1=BFS  2=Greedy  3=A*)", True, (255, 255, 255)
    )
    text2 = font.render(
        mode_text_map.get(edit_mode, ""), True, (200, 200, 200)
    )
    text3 = font.render("R: Reset | Fare + O/S/G/T ile haritayı canlı düzenle", True, (200, 200, 200))

    screen.blit(text1, (10, 5))
    screen.blit(text2, (10, 25))
    screen.blit(text3, (10, 45))

    pygame.display.flip()

pygame.quit()
sys.exit()
