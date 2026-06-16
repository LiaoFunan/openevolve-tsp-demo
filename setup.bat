@echo off
REM ============================================================
REM   一鍵安裝腳本(Windows)
REM   用法:在 repo 資料夾裡雙擊 setup.bat,或在命令列執行 setup.bat
REM ============================================================

echo.
echo ======================================
echo   OpenEvolve TSP Demo -- 環境安裝
echo ======================================
echo.

REM ---- 檢查 Ollama ----
where ollama >nul 2>nul
if errorlevel 1 (
    echo [X] 找不到 Ollama。請先到 https://ollama.com 下載安裝,再重跑這個腳本。
    pause
    exit /b 1
)
echo [OK] 偵測到 Ollama

REM ---- 檢查 Python ----
where python >nul 2>nul
if errorlevel 1 (
    echo [X] 找不到 python。請先安裝 Python 3.10 以上,並勾選 Add to PATH。
    pause
    exit /b 1
)
echo [OK] 偵測到 Python

echo.
echo [1/3] 安裝 OpenEvolve 與相依套件...
pip install openevolve matplotlib -q

echo.
echo [2/3] 下載本地模型 qwen2.5-coder:7b(約 4.7GB,第一次下載請耐心等)...
ollama pull qwen2.5-coder:7b

echo.
echo [3/3] 測試環境(跑一次評分)...
python evaluator.py

echo.
echo ======================================
echo   [OK] 安裝完成!
echo.
echo   開始演化請執行:
echo     python run.py
echo ======================================
echo.
pause
