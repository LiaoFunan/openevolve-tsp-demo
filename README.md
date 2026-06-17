# OpenEvolve TSP Demo —— 用本地 LLM 演化「最短路徑」演算法

這是一個**課堂示範專案**:讓你電腦上的本地 LLM(透過 Ollama)一代一代地
改寫一支求解 **TSP 旅行推銷員問題**的程式,親眼看它從「亂繞的爛路線」
演化成「漂亮又短的環」。

> **TSP 是什麼?** 有一堆城市,要拜訪每個城市一次再回到起點,問怎麼走總距離最短。
> 初始程式用很笨的「最近鄰法」,OpenEvolve 會讓 LLM 自動加入 2-opt、模擬退火等技巧把路線縮短。

整個過程**完全在你自己電腦上跑**:不用註冊、不用 API key、不用網路(模型下載完之後)。

---

## 一、事前需求(請在上課前裝好)

1. **Ollama** —— 到 https://ollama.com 下載安裝(Windows / Mac / Linux 都有)
2. **Python 3.10 以上** —— https://www.python.org(Windows 安裝時請勾選 *Add to PATH*)
3. 一張 **顯卡**(NVIDIA 8GB VRAM 以上即可,RTX 4000 系列都沒問題)

---

## 二、安裝(課前一定要先做完!)

> ⚠️ **重要:第 2 步會下載約 4.7GB 的模型,請務必在上課前先在家裡網路下載好。**
> 不要等到課堂現場才下載,以免卡住跟不上進度。

**下載這個專案:**
```bash
git clone https://github.com/LiaoFunan/openevolve-tsp-demo.git
cd openevolve-tsp-demo
```

**Mac / Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```
雙擊 setup.bat   (或在命令列執行 setup.bat)
```

腳本會自動:安裝 OpenEvolve → 下載模型 → 跑一次測試。
看到最後出現 `✅ 安裝完成!` 就代表環境 OK。

---

## 三、開始演化

```bash
python run.py
```

你會看到一代一代的日誌,**分數慢慢往上爬**(初始約 0.75,會越來越接近 1.0 甚至更高),
代表 LLM 找到的路線越來越短。

跑的同時,打開資料夾裡的 **`route.png`**,它會即時更新——
你會看到路線從**雜亂交叉**慢慢變成**乾淨的環**,這就是演化的成果。

跑完後:
- 最佳程式: `openevolve_output/best/best_program.py`
- 最佳路線圖: `route.png`

---

## 四、檔案說明

| 檔案 | 作用 |
|---|---|
| `initial_program.py` | 演化的**起點**(很笨的最近鄰法,被 LLM 改寫的就是這支) |
| `evaluator.py` | **評分**:路線越短分數越高;同時畫出 `route.png` |
| `config.yaml` | 設定:連本機 Ollama、用哪個模型、演化幾代 |
| `run.py` | 一鍵啟動演化(命令列用) |
| `demo.ipynb` | **教學用 Notebook**:一格一格看演化過程,適合課堂講解 / 自學 |
| `requirements.txt` | Python 套件清單(`pip install -r requirements.txt`) |
| `setup.sh` / `setup.bat` | 一鍵安裝 |
| `.vscode/` | VS Code 設定:按 F5 直接執行、自動推薦安裝 Python/Jupyter 擴充 |

> **用 VS Code 開啟建議**:直接用 **Windows 原生**開啟(不要用 WSL)。
> 因為 Ollama 跑在 Windows 的 `localhost:11434`,WSL 連回去要額外設轉址,容易卡。
>
> **兩種用法**:想直接跑就用 `python run.py`;想一步一步看懂演化過程就開 `demo.ipynb`。

---

## 五、課堂前自我檢查清單 ✅

上課前請確認以下每一項都打勾,當天才能順利跟上:

- [ ] Ollama 已安裝(命令列打 `ollama --version` 有反應)
- [ ] Python 已安裝(命令列打 `python --version` 顯示 3.10+)
- [ ] 已 clone 本專案並跑完 `setup.sh` / `setup.bat`
- [ ] 看到 `✅ 安裝完成!`
- [ ] 試跑過一次 `python run.py`,有看到分數在動

---

## 六、常見問題

**Q：跑 `run.py` 一直卡住沒反應?**
A：確認 Ollama 服務有開著。命令列執行 `ollama list`,要能看到 `codegemma:2b`。
   如果沒有,跑 `ollama pull codegemma:2b` 重新下載。

**Q：顯卡是 20GB 以上(RTX 4000 Ada / Blackwell),想要更好的效果?**
A：把 `config.yaml` 裡的 `model` 改成 `codegemma:7b`,
   並先 `ollama pull codegemma:7b`。7B 的演化品質更好。

**Q：跑很慢?**
A：8GB 顯卡跑 7B 屬正常稍慢。若想更快可改 `config.yaml` 把 `max_iterations` 調小,
   (codegemma:2b 已是小模型,若仍慢可把 `max_iterations` 調小)。

**Q：分數沒怎麼進步?**
A：LLM 演化有隨機性,偶爾某幾代沒進展是正常的。多跑幾代、或把 `max_iterations` 調大即可。
