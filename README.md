# OpenEvolve TSP Demo —— 用本地 LLM 演化「最短路徑」演算法

這是一個**課堂示範專案**:讓你電腦上的本地 LLM(透過 Ollama)一代一代地
改寫一支求解 **TSP 旅行推銷員問題**的程式,親眼看它從「亂繞的爛路線」
演化成「漂亮又短的環」。

> **TSP 是什麼?** 有一堆城市,要拜訪每個城市一次再回到起點,問怎麼走總距離最短。
> 初始程式用很笨的「最近鄰法」,OpenEvolve 會讓 LLM 自動加入 2-opt、模擬退火等技巧把路線縮短。

整個過程**完全在你自己電腦上跑**:不用註冊、不用 API key、不用網路(模型下載完之後)。

---

## 一、事前需求(國立中興大學資訊科學大樓 701 電腦教室的 Windows 版已經有了，但如果你想在自己的電腦上試請前準備好)

1. 一張 **顯卡**(NVIDIA 8GB VRAM 以上即可,RTX 4000 系列都沒問題)
2. Visual Studio Code https://code.visualstudio.com/
3. 如果電腦裡沒有 Git 可打開 Visual Studio Code 後點擊左方的 Source Control 按鈕依指示安裝：

<img width="400" height="368" alt="image" src="https://github.com/user-attachments/assets/fa336306-fd63-48ee-8e8c-dd6de24d5b55" />

或直接去 https://git-scm.com/ 下載安裝也可以。

---

## 二、Clone 本專案

點擊本專案左上方 Code 按鈕，然後點 Copy URL to clipboard 複製網址

<img width="1295" height="660" alt="image" src="https://github.com/user-attachments/assets/b919ea34-44a3-4f84-ac8e-d5d462441350" />

打開 Visual Studio Code 後點擊左方的 Source Control 按鈕再點擊 Clone Repository 按鈕，然後把剛剛複製的網址貼上去

<img width="706" height="368" alt="image" src="https://github.com/user-attachments/assets/d7595073-be67-40e4-ad5b-59fe9481f6ae" />

隨便選一個之後要用來放程式的資料夾，我這裡選 PyCharmMiscProject

<img width="946" height="533" alt="image" src="https://github.com/user-attachments/assets/b379836b-e0b1-4701-a8af-5d5701988e60" />

點 Open

<img width="364" height="125" alt="image" src="https://github.com/user-attachments/assets/e2ea2da7-af1f-4221-8169-04326c477eff" />

點 Yes, I trust the authors

<img width="706" height="544" alt="image" src="https://github.com/user-attachments/assets/9dc0be00-1ec5-4611-a0d0-00b020f725a1" />

點 Install

<img width="706" height="544" alt="image" src="https://github.com/user-attachments/assets/0f1b285c-45ed-46b7-aed0-70d5e692180e" />

---

## 二、建 environment 及安裝 OpenEvolve

非必要，但開始用 Pyhton 寫程式之後系統可能會開始有一大堆 python.exe，很難說它們會不會被放到 PATH 裡？被放到 PATH 裡的那個是不是你現在在用的那個... 等等。為了跳過無聊的鬧劇，也避免你在別人的電腦上跑的時候改到別人的設定，新建一個 environment 是比較簡單的選擇。

點開隨便一個 .py 檔案，這裡我們點 evaluator.py。然後點右下角的 Python 3.14 (64-bit)

<img width="1010" height="436" alt="image" src="https://github.com/user-attachments/assets/f89464da-ac3b-4602-a709-46b3267a7109" />

點 Create Virtual Environment...

<img width="1010" height="464" alt="image" src="https://github.com/user-attachments/assets/b328aeb1-b1c4-4e84-96f2-09e0894509fc" />

我個人會選 Conda。如果這裡沒有 Conda 的選項，可以去 https://www.anaconda.com/ 下載安裝再從頭來一次

<img width="1010" height="464" alt="image" src="https://github.com/user-attachments/assets/cd5ff77f-aa4f-439e-817b-648129ddaa38" />

選 Prefix 就好

<img width="1010" height="464" alt="image" src="https://github.com/user-attachments/assets/09549f1e-b7ee-4de5-8fe1-2b870dfe820e" />

選最新的，這裡是 Python 3.14.2

<img width="1010" height="464" alt="image" src="https://github.com/user-attachments/assets/789ecdb3-a5ab-496d-a949-75f3f75ac440" />

點 Terminal 內的 New Terminal

<img width="1408" height="465" alt="image" src="https://github.com/user-attachments/assets/04d29bd9-0367-4ba7-a148-660f7ba993d8" />

點 + 選 Command Prompt

<img width="1408" height="465" alt="image" src="https://github.com/user-attachments/assets/c4160e18-68d0-4e8f-837b-e47caf203e54" />

輸入 pip install openevolve matplotlib 按下 Enter 以安裝 OpenEvolve
<img width="1622" height="1032" alt="image" src="https://github.com/user-attachments/assets/b81da15b-e7a1-4979-93fb-646c7cd57548" />

看到下面這個畫面就是裝完了

<img width="1622" height="1032" alt="image" src="https://github.com/user-attachments/assets/377f1194-81bb-4568-b2d5-52b5da1dd4a1" />

---

## 三、安裝 Ollama 及模型

- 到 https://ollama.com 下載安裝，安裝完直接關掉就好。
- 關掉 Visual Studio Code 再重新打開，以便 Visual Studio Code 讀到 Ollama 的路徑。
- 點 Terminal 內的 New Terminal；點 + 選 Command Prompt；輸入 ollama pull qwen2.5-coder:7b 按下 Enter 以下載千問程式模型(約 4.7GB)。第一次會比較久,請耐心等到出現 success。這個模型在「小模型寫 diff」這件事上最穩,演化才跑得動。 顯卡夠力(20GB+)可改成 qwen2.5-coder:14b(config.yaml 也要一起改)。

<img width="1622" height="523" alt="image" src="https://github.com/user-attachments/assets/f26fba3f-ab03-4374-ace1-33fd44cf44e8" />

---

## 四、開始演化

點開 run.py 並點右上角的三角形開始執行

<img width="1622" height="523" alt="image" src="https://github.com/user-attachments/assets/fed3bf90-877b-419c-baf7-c76cedadb852" />

如果執行出問題的話，可以去控制台檢查看看"Beta: 使用 Unicode 提供全球語言技援"有沒有打勾

<img width="1920" height="1032" alt="image" src="https://github.com/user-attachments/assets/237acced-88e4-46cf-9867-2c991ea7ada2" />

如果執行順利的話，你會看到一代一代的日誌,**分數慢慢往上爬**(初始約 0.75,會越來越接近 1.0 甚至更高),
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
