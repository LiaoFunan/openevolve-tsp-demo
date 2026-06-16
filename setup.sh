#!/bin/bash
# ============================================================
#  一鍵安裝腳本(Mac / Linux)
#  用法:在 repo 資料夾裡執行  ./setup.sh
# ============================================================
set -e

echo ""
echo "======================================"
echo "  OpenEvolve TSP Demo —— 環境安裝"
echo "======================================"
echo ""

# ---- 檢查 Ollama 有沒有裝 ----
if ! command -v ollama &> /dev/null; then
    echo "❌ 找不到 Ollama。請先到 https://ollama.com 下載安裝,再重跑這個腳本。"
    exit 1
fi
echo "✅ 偵測到 Ollama"

# ---- 檢查 Python ----
if ! command -v python3 &> /dev/null; then
    echo "❌ 找不到 python3。請先安裝 Python 3.10 以上。"
    exit 1
fi
echo "✅ 偵測到 Python"

# ---- 安裝 OpenEvolve 與繪圖套件 ----
echo ""
echo "[1/3] 安裝 OpenEvolve 與相依套件..."
pip install openevolve matplotlib -q

# ---- 下載模型(約 4.7GB,第一次會比較久) ----
echo ""
echo "[2/3] 下載本地模型 qwen2.5-coder:7b(約 4.7GB,第一次下載請耐心等)..."
ollama pull qwen2.5-coder:7b

# ---- 快速自測:確認 evaluator 跑得起來 ----
echo ""
echo "[3/3] 測試環境(跑一次評分)..."
python3 evaluator.py

echo ""
echo "======================================"
echo "  ✅ 安裝完成!"
echo ""
echo "  開始演化請執行:"
echo "    python3 run.py"
echo "======================================"
echo ""
