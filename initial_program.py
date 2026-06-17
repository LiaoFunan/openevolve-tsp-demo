# EVOLVE-BLOCK-START
"""
TSP 求解器 —— 演化起點(刻意寫得很笨)

任務:給定一組城市座標,找出「拜訪每個城市一次並回到起點」的最短路線。

這個初始版本用「最近鄰法 (Nearest Neighbor)」:
每次都貪心地走到最近、還沒去過的城市。
這方法很快,但常常繞遠路、會留下交叉的路線,結果通常不是最佳解。

OpenEvolve 會讓 LLM 一代一代改寫下面這個 solve() 函式,
加入像 2-opt、模擬退火、多起點重啟等技巧,讓總路線越來越短。

★ 改寫時的硬性規則(務必遵守,否則程式會跑不動被淘汰):
  1. 保留所有 import,要用到 random 就一定要 import random、要用 math 就 import math。
  2. 函式簽名固定 def solve(cities):,參數名一定是 cities,不可改名。
  3. 只能用傳入的 cities,不要用未定義的全域變數。
  4. 回傳城市索引清單,每個索引(0..n-1)恰好出現一次。
"""

import math
import random  # 預留:演化常用到隨機(多起點、shuffle 等),先 import 避免漏掉


def distance(a, b):
    """兩個城市之間的歐式距離"""
    return math.hypot(a[0] - b[0], a[1] - b[1])


def tour_length(tour, cities):
    """計算一條封閉路線的總長度(最後會回到起點)"""
    total = 0.0
    for i in range(len(tour)):
        a = cities[tour[i]]
        b = cities[tour[(i + 1) % len(tour)]]
        total += distance(a, b)
    return total


def solve(cities):
    """
    輸入: cities —— 城市座標清單,例如 [(x0, y0), (x1, y1), ...]
    輸出: tour   —— 一個拜訪順序(城市索引的清單),
                     例如 [0, 3, 1, 2, ...],代表先去城市0、再去城市3...

    >>> 這就是被演化的核心。目前是最近鄰法,很笨,請改進它。 <<<
    """
    n = len(cities)
    if n == 0:
        return []

    unvisited = set(range(n))
    current = 0                 # 從城市 0 出發
    tour = [current]
    unvisited.remove(current)

    # 貪心:每一步都跳到最近的未訪城市
    while unvisited:
        nearest = min(unvisited, key=lambda c: distance(cities[current], cities[c]))
        tour.append(nearest)
        unvisited.remove(nearest)
        current = nearest

    return tour
# EVOLVE-BLOCK-END


# ----- 以下不被演化,給本機自測用 -----
if __name__ == "__main__":
    import random
    random.seed(0)
    demo_cities = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(20)]
    t = solve(demo_cities)
    print("路線:", t)
    print("總長度:", round(tour_length(t, demo_cities), 2))
