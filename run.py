"""
一鍵啟動演化。

學生只要執行:  python run.py

它會用 config.yaml 的設定,讓本機 Ollama 的 LLM
一代一代改寫 initial_program.py 裡的 solve(),
目標是找出更短的 TSP 路線(分數越高越好)。

跑完後最佳程式會存在 openevolve_output/best/best_program.py,
而每次評分產生的路線圖會存在 route.png(可隨時打開看當前最好的路線)。
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    try:
        from openevolve import run_evolution
    except ImportError:
        print("❌ 還沒安裝 OpenEvolve。請先執行 setup.sh(Mac/Linux)或 setup.bat(Windows)。")
        sys.exit(1)

    print("開始演化…(每一代會印出分數,路線圖即時更新在 route.png)\n")

    run_evolution(
        initial_program=os.path.join(HERE, "initial_program.py"),
        evaluator=os.path.join(HERE, "evaluator.py"),
        config=os.path.join(HERE, "config.yaml"),
    )

    print("\n✅ 演化完成!")
    print("   最佳程式: openevolve_output/best/best_program.py")
    print("   最佳路線圖: route.png")


if __name__ == "__main__":
    main()
