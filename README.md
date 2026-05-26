# Wafer-Pro 半導體缺陷整合專家診斷系統 (Static Web Version)

這是一個基於 HTML5 / CSS3 / ES6 JavaScript 的**高響應度無伺服器（Serverless）半導體缺陷專家診斷儀表板**。

移植自原先的 Python Streamlit 版本，本版本已被完全重構為**純靜態網頁應用**。所有評分邏輯、Boost 機制、SVG 失效拓撲繪製與 Radar 機率多邊形渲染，皆在瀏覽器端本地進行（運算速度低於 10ms），不需依賴任何 Python 後端伺服器與資料庫，且支援完全離線使用。

---

## 🌟 核心特色


1. **零延遲計算與雙向資料同步**
   - 動態雙向綁定輸入：調整滑桿（Slider）或精確數值輸入框（Number Input）時，數值與對應的 Evidence 得分即時雙向同步。
   - 所有診斷結果、候選缺陷機率條、即時監控看板、推理路徑與文字報告均在 **10 毫秒內**瞬間重新運算並更新。

2. **動態物理失效視覺化**
   - **晶片物理失效拓撲圖**：根據診斷出機率最高的缺陷，動態以 SVG 渲染出晶片微觀結構的物理故障路徑（如 Bridging 殘留跨橋、Open 斷線、Oxide 電漿擊穿、Latch-up 熱點等）。
   - **六邊形 Radar 機率分佈圖**：動態計算六大核心缺陷大類（Bridge, Open, Overlay, Oxide, Thermal, Material）的機率分佈並重新繪製多邊形發光網格。

3. **一鍵導出報告**
   - 整合純前端下載與複製機制，一鍵即可生成 Markdown 格式的完整失效分析與改善建議報告，方便貼入工程 Lot log 或發送郵件。

---

## 📁 專案結構

```text
├── index.html        # 系統的核心單網頁（內含完整 HTML5 結構、控制台 CSS3 樣式與 ES6 診斷 JS 引擎）
├── README.md         # 專案說明文件
└── .gitignore        # Git 忽略檔案清單
```
