"""
TSP evaluator —— 評分程式

OpenEvolve 每產生一個新版本的 initial_program.py,就會呼叫這裡的 evaluate(),
拿到一個分數(越高越好)。OpenEvolve 會朝「分數越高」的方向演化。

評分邏輯:
  - 用一組「固定的城市座標」(寫死,確保每個學生、每一代都公平比較)
  - 跑出來的路線越短 → 分數越高
  - 分數 = 參考長度 / 實際長度   (所以實際路線越短,分數越接近甚至超過 1)
  - 如果路線非法(漏城市、重複、格式錯) → 給 0 分

順便:每次評分會把當前路線畫成一張圖存到 route.png,
這樣學生可以親眼看到路線從「亂繞」慢慢變成「漂亮的環」。
"""

import importlib.util
import math
import os
import random

# ---- 固定城市座標:30 個城市,seed 寫死,全班一致 ----
_rng = random.Random(42)
CITIES = [(_rng.uniform(0, 100), _rng.uniform(0, 100)) for _ in range(30)]

# 一個參考長度,純粹用來把分數正規化到好看的範圍。
# 故意設得比「最近鄰法的結果」短一些,讓初始版本分數偏低(~0.75),
# 這樣學生才看得到分數一代代往上爬、越來越接近 1.0 的演化過程。
_REFERENCE_LENGTH = 380.0


def _distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _tour_length(tour):
    total = 0.0
    for i in range(len(tour)):
        a = CITIES[tour[i]]
        b = CITIES[tour[(i + 1) % len(tour)]]
        total += _distance(a, b)
    return total


def _is_valid(tour):
    """路線必須剛好是 0..n-1 的一個排列(每個城市恰好一次)"""
    return sorted(tour) == list(range(len(CITIES)))


def _plot_route(tour, length, out_path):
    """把路線畫出來(失敗就安靜跳過,不影響評分)"""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        xs = [CITIES[i][0] for i in tour] + [CITIES[tour[0]][0]]
        ys = [CITIES[i][1] for i in tour] + [CITIES[tour[0]][1]]

        plt.figure(figsize=(6, 6))
        plt.plot(xs, ys, "-o", linewidth=1.5, markersize=5)
        plt.title(f"TSP route — total length = {length:.1f}")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.tight_layout()
        plt.savefig(out_path, dpi=110)
        plt.close()
    except Exception:
        pass


def evaluate(program_path):
    """
    OpenEvolve 會呼叫這個函式。
    回傳一個 dict,至少包含 'combined_score'(OpenEvolve 用它來演化)。
    """
    # 動態載入被演化的程式
    spec = importlib.util.spec_from_file_location("candidate", program_path)
    candidate = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(candidate)
        tour = candidate.solve(CITIES)
    except Exception as e:
        # 程式跑爛了 → 0 分,並把錯誤回傳給 LLM 當改進線索
        return {"combined_score": 0.0, "error": f"執行失敗: {e}"}

    # 路線合法性檢查
    if not isinstance(tour, list) or not _is_valid(tour):
        return {
            "combined_score": 0.0,
            "error": "路線非法:必須是每個城市恰好出現一次的索引清單",
        }

    length = _tour_length(tour)
    score = _REFERENCE_LENGTH / length if length > 0 else 0.0

    # 畫圖(存在跟程式同層的資料夾,方便學生查看)
    out_dir = os.path.dirname(os.path.abspath(program_path))
    _plot_route(tour, length, os.path.join(out_dir, "route.png"))

    return {
        "combined_score": score,   # 越高越好;路線越短,這個值越大
        "tour_length": length,     # 給人看的實際總長度(越小越好)
    }


# ----- 本機自測 -----
if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    result = evaluate(os.path.join(here, "initial_program.py"))
    print("評分結果:", result)
    print("(route.png 已輸出,可打開看初始路線長怎樣)")
