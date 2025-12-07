import sys
import pygame
from collections import deque
import heapq

# ======================
# 1) HARİTA, IŞIK, YARDIMCI FONKSİYONLAR
# ======================


# 0 = yol, 1 = engel, S = başlangıç, G = hedef, T = trafik ışığı
grid = [
    ['S', 0,   0,   0,   0,   0,   0,   0,   0,   0],
    [0,   1,   1,   1,   0,   1,   0,   1,   1,   0],
    [0,   0,   0,   1,  'T',  1,   0,   0,   0,   0],
    [1,   1,   0,   1,   0,   1,   1,   1,   0,   1],
    [0,   0,   0,   0,   0,   0,   0,   1,   0,   0],
    [0,   1,   1,   1,   1,   1,   0,   1,   0,   1],
    [0,   0,   0,   0,   0,   0,   0,   1,   0,   0],
    [0,   1,   1,   1,   1,   1,   0,   0,   0,  'G'],
]

ROWS = len(grid)
COLS = len(grid[0])


class TrafficLight:
    def __init__(self, position, red_time=3, green_time=3):
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


# ==========
# 2) ALGORİTMALAR
# ==========

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


def compute_path(algo_name, start, goal):
    if algo_name == "BFS":
        return bfs(grid, start, goal)
    elif algo_name == "Greedy":
        return greedy_path(grid, start, goal)
    elif algo_name == "A*":
        return astar_path(grid, start, goal)
    else:
        return []


start, goal = find_start_goal(grid)
traffic_light = TrafficLight((2, 4), red_time=3, green_time=3)

current_algo = "BFS"
path = compute_path(current_algo, start, goal)

# Dinamik engel değişkenleri
dynamic_obstacle_created = False
dynamic_obstacle_pos = None

# ======================
# 3) PYGAME AYARLARI
# ======================

pygame.init()

CELL_SIZE = 60  
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE + 40  

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Otonom Araç Simülasyonu - Dinamik Engel + 3 Algoritma")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

path_index = 0
running = True

while running:
    clock.tick(3)  # biraz daha akıcı hareket (3 FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_algo = "BFS"
            elif event.key == pygame.K_2:
                current_algo = "Greedy"
            elif event.key == pygame.K_3:
                current_algo = "A*"

            # Algoritma değişince her şeyi resetle
            path = compute_path(current_algo, start, goal)
            path_index = 0
            dynamic_obstacle_created = False
            dynamic_obstacle_pos = None
            grid = [row[:] for row in [
                ['S', 0,   0,   0,   0,   0,   0,   0,   0,   0],
                [0,   1,   1,   1,   0,   1,   0,   1,   1,   0],
                [0,   0,   0,   1,  'T',  1,   0,   0,   0,   0],
                [1,   1,   0,   1,   0,   1,   1,   1,   0,   1],
                [0,   0,   0,   0,   0,   0,   0,   1,   0,   0],
                [0,   1,   1,   1,   1,   1,   0,   1,   0,   1],
                [0,   0,   0,   0,   0,   0,   0,   1,   0,   0],
                [0,   1,   1,   1,   1,   1,   0,   0,   0,  'G'],
            ]]

    # Yol yoksa araba start'ta dursun
    if not path:
        car_r, car_c = start
    else:
        traffic_light.update()

        # ---------- DİNAMİK ENGEL (güvenli) ----------
        # Araç biraz ilerlesin, sonra yolun İLERİSİNE engel koymayı dene
        if (not dynamic_obstacle_created) and path_index >= 4 and len(path) > path_index + 3:
            candidate_pos = path[path_index + 3]
            cr, cc = candidate_pos

            if grid[cr][cc] == 0:
                # Geçici olarak engel koy
                old_value = grid[cr][cc]
                grid[cr][cc] = 1

                current_pos = path[path_index]
                new_path = compute_path(current_algo, current_pos, goal)

                if new_path:
                    # Yeni yol bulundu -> dinamik engel kalıcı
                    dynamic_obstacle_created = True
                    dynamic_obstacle_pos = candidate_pos
                    path = new_path
                    path_index = 0
                else:
                    # Yol tamamen kapanıyorsa engeli geri al
                    grid[cr][cc] = old_value

        # Arabanın mevcut konumu
        car_r, car_c = path[path_index]

        # Trafik ışığı kontrolü
        if (car_r, car_c) == traffic_light.position and traffic_light.is_red():
            pass  # kırmızıda bekle
        else:
            if path_index < len(path) - 1:
                path_index += 1
                car_r, car_c = path[path_index]

    # ======================
    # 4) ÇİZİM
    # ======================

    screen.fill((25, 25, 30))  # koyu arka plan

    # Haritayı çiz
    for r in range(ROWS):
        for c in range(COLS):
            cell = grid[r][c]
            rect = pygame.Rect(
                c * CELL_SIZE,
                r * CELL_SIZE + 40,   # üstte yazı alanı için 40 piksel kaydır
                CELL_SIZE,
                CELL_SIZE
            )

            if cell == 1:
                # Dinamik engel ise farklı renkte göster
                if dynamic_obstacle_pos == (r, c):
                    color = (180, 40, 40)   # kırmızımsı dinamik engel
                else:
                    color = (80, 80, 80)    # normal engel
            elif cell == 'S':
                color = (0, 80, 220)        # başlangıç
            elif cell == 'G':
                color = (0, 180, 0)         # hedef
            elif cell == 'T':
                if traffic_light.is_red():
                    color = (220, 40, 40)   # kırmızı ışık
                else:
                    color = (60, 200, 60)   # yeşil ışık
            else:
                color = (50, 50, 60)        # normal yol

            pygame.draw.rect(screen, color, rect, border_radius=8)
            pygame.draw.rect(screen, (100, 100, 110), rect, 1)

    # YOLU ÇİZGİ OLARAK GÖSTER 
    if len(path) > 1:
        points = []
        for (pr, pc) in path:
            x = pc * CELL_SIZE + CELL_SIZE // 2
            y = pr * CELL_SIZE + 40 + CELL_SIZE // 2
            points.append((x, y))
        pygame.draw.lines(screen, (0, 140, 255), False, points, 3)

    # ARACI ÇİZ
    car_x = car_c * CELL_SIZE + CELL_SIZE // 2
    car_y = car_r * CELL_SIZE + 40 + CELL_SIZE // 2
    car_radius = CELL_SIZE // 3
    pygame.draw.circle(screen, (255, 230, 0), (car_x, car_y), car_radius)

    # BİLGİ YAZILARI
    text_alg = font.render(f"Algoritma: {current_algo}  (1:BFS  2:Greedy  3:A*)", True, (255, 255, 255))
    screen.blit(text_alg, (10, 10))

    if dynamic_obstacle_created:
        text_dyn = font.render("Dinamik engel: kırmızı blok (rota yeniden hesaplandı)", True, (255, 200, 0))
        screen.blit(text_dyn, (10, HEIGHT - 25))

    pygame.display.flip()

pygame.quit()
sys.exit()
