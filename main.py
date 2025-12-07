print("Otonom araba projesi başlıyor!")

# Harita matrisi (grid)
grid = [
    ['S', 0,   0,   0,   1,   0,   0],
    [0,   1,   1,   'T', 1,   0,   0],
    [0,   0,   0,   0,   0,   0,   0],
    [1,   1,   0,   1,   1,   1,   0],
    [0,   0,   0,   0,   0,   0,  'G'],
]


# Haritayı ekrana yazdır
def print_grid(g):
    for row in g:
        print(row)

print("Harita:")
print_grid(grid)

# Başlangıç ve hedef bul
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

start, goal = find_start_goal(grid)
print("Başlangıç (S):", start)
print("Hedef (G):", goal)

def is_free(g, r, c):
    if r < 0 or c < 0 or r >= len(g) or c >= len(g[0]):
        return False

    cell = g[r][c]
    if cell == 0 or cell == 'S' or cell == 'G':
        return True
    else:
        return False


def manhattan(a, b):
    # a ve b: (satır, sütun)
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

import heapq
from collections import deque

def bfs(g, start, goal):
    queue = deque()
    queue.append(start)

    visited = set()
    visited.add(start)

    prev = {}

    directions = [(-1,0),(1,0),(0,-1),(0,1)]

    while queue:
        current = queue.popleft()

        if current == goal:
            break

        r, c = current

        for dr, dc in directions:
            nr = r + dr
            nc = c + dc
            neighbour = (nr, nc)

            if is_free(g, nr, nc) and neighbour not in visited:
                visited.add(neighbour)
                prev[neighbour] = current
                queue.append(neighbour)

    if goal not in visited:
        return []

    path = []
    current = goal
    while current != start:
        path.append(current)
        current = prev[current]
    path.append(start)

    path.reverse()
    return path


def greedy_path(g, start, goal, max_steps=500):
    current = start
    path = [current]
    visited = set([current])

    directions = [(-1,0),(1,0),(0,-1),(0,1)]

    for _ in range(max_steps):
        if current == goal:
            break

        r, c = current
        best_neighbour = None
        best_h = float('inf')

        for dr, dc in directions:
            nr = r + dr
            nc = c + dc
            neighbour = (nr, nc)

            if not is_free(g, nr, nc):
                continue
            if neighbour in visited:
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
        print("Greedy algoritma hedefe ulaşamadı veya takıldı.")
    return path

def astar_path(g, start, goal):
    # open_set: (f_score, (r, c)) şeklinde tutulacak
    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {start: None}
    g_score = {start: 0}

    directions = [(-1,0),(1,0),(0,-1),(0,1)]

    while open_set:
        # En küçük f_score'a sahip olan düğümü al
        _, current = heapq.heappop(open_set)

        if current == goal:
            break

        r, c = current

        for dr, dc in directions:
            nr = r + dr
            nc = c + dc
            neighbour = (nr, nc)

            if not is_free(g, nr, nc):
                continue

            # g_score: başlangıçtan buraya kadar olan gerçek maliyet
            tentative_g = g_score[current] + 1  # her adımın maliyeti 1

            if neighbour not in g_score or tentative_g < g_score[neighbour]:
                g_score[neighbour] = tentative_g
                f_score = tentative_g + manhattan(neighbour, goal)  # g + h
                heapq.heappush(open_set, (f_score, neighbour))
                came_from[neighbour] = current

    # Hedefe hiç ulaşamamışsak
    if goal not in came_from:
        return []

    # Yol geri sarma
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path

print("\n--- BFS algoritma ---")


path = bfs(grid, start, goal)
print("Bulunan yol:")
print(path)

def mark_path_on_grid(g, path):
    new_grid = [row[:] for row in g]
    for (r, c) in path:
        if new_grid[r][c] == 0:  # sadece yollara * koy
            new_grid[r][c] = '*'
    return new_grid

marked = mark_path_on_grid(grid, path)
print("Yol işaretlenmiş harita:")
print_grid(marked)

print("\n--- Greedy algoritma ---")
g_path = greedy_path(grid, start, goal)
print("Greedy yol:")
print(g_path)
print("Greedy yol uzunluğu:", len(g_path))

g_marked = mark_path_on_grid(grid, g_path)
print("Greedy yol işaretlenmiş harita:")
print_grid(g_marked)

print("\n--- A* algoritma ---")
a_path = astar_path(grid, start, goal)
print("A* yol:")
print(a_path)
print("A* yol uzunluğu:", len(a_path))

a_marked = mark_path_on_grid(grid, a_path)
print("A* yol işaretlenmiş harita:")
print_grid(a_marked)
