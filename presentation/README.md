# presenter-mode-reveal · 演講者模式範本

一份專為**帶逐字稿的技術分享**設計的 full-deck 範本。核心賣點是真正可用的**磁吸卡片式演講者視圖**：當前頁 iframe 預覽 + 下頁 iframe 預覽 + 大字號逐字稿 + 計時器，4 個卡片可任意拖曳/縮放，全部整合在 `runtime.js` 裡，零依賴。

## 使用場景

- 技術分享 / tech talk（30-60 min）
- 產品發布會主講
- 課程講授
- 任何**需要照著講、但不能念稿**的正式演講

## 快速開始

```bash
cp -r templates/full-decks/presenter-mode-reveal examples/my-talk
open examples/my-talk/index.html
```

## 鍵盤操作

| 鍵 | 動作 |
|---|---|
| `S` | 打開演講者視窗（彈出新視窗，原頁面不動） |
| `T` | 切換主題（5 種預設） |
| `←` `→` | 翻頁 |
| `Space` / `PgDn` | 下一頁 |
| `F` | 全螢幕 |
| `O` | 總覽縮圖 |
| `R` | 重置計時器（僅演講者視圖下） |
| `Esc` | 關閉所有浮層 |

## 主題切換

範本預設了 5 個適配演講場景的主題，在 `<html data-themes="...">` 屬性裡：

```html
<html lang="zh-TW" data-themes="tokyo-night,dracula,catppuccin-mocha,nord,corporate-clean">
```

按 `T` 循環切換。可以改成任何 `assets/themes/*.css` 裡的主題。

## 寫逐字稿的規範

**每一頁的 `<aside class="notes">` 裡寫 150–300 字**。三條鐵律：

1. **不是講稿，是提示信號** — 核心點加粗、過渡句成段、數據列清楚
2. **150–300 字/頁** — 按 2–3 分鐘/頁的節奏
3. **用口語寫** — "因此" → "所以"；"該方案" → "這個方案"；讀一遍不拗口才對

範例：
```html
<aside class="notes">
  <p>大家好，今天跟大家聊一個 <strong>很多人忽略的問題</strong>——...</p>
  <p>我先拋一個觀點：<em>做 PPT 和講 PPT 是兩件事</em>。</p>
  <p>接下來我會用 3 個例子證明這個觀點...</p>
</aside>
```

支援的 inline 標籤：
- `<strong>` — 高亮（橘色）
- `<em>` — 斜體強調（藍色）
- `<code>` — 等寬字體
- `<p>` — 分段（推薦每段講 30-60 秒的內容）

## 檔案結構

```
presenter-mode-reveal/
├── index.html       # 6 張範例 slide，每頁都有完整逐字稿
├── style.css        # scoped .tpl-presenter-mode-reveal 樣式
└── README.md        # 本檔案
```

## 修改 / 擴展

- **加頁**：複製任意 `<section class="slide">` 區塊，改內容和 `<aside class="notes">`
- **換主題**：改 `data-themes` 列表，或直接改 `<link id="theme-link" href="...">`
- **改樣式**：只動 `style.css`，不要碰根目錄的 `assets/base.css`
- **加動效**：在元素上加 `data-anim="fade-up"` 等（參考 `references/animations.md`）

## 演講者視窗的 4 個卡片

按 `S` 後彈出的視窗裡有：

- 🔵 **CURRENT** — 當前頁 iframe 預覽（加載 `?preview=N` 模式，像素級完美，與觀眾端同 CSS/主題/字體）
- 🟣 **NEXT** — 下一頁預覽，幫助準備過渡
- 🟠 **SPEAKER SCRIPT** — 大字號逐字稿，可滾動
- 🟢 **TIMER** — 經過時間 + 頁碼 + Prev/Next/Reset 按鈕

卡片操作：
- **拖曳卡片頭**（彩色圓點 + 標題的頂部條）→ 移動卡片
- **拖曳卡片右下角** → 調整大小
- 位置 + 尺寸自動存 localStorage，下次打開恢復
- 底部 "重置佈局" 按鈕可恢復預設卡片排列

翻頁絲滑：iframe 只加載一次，後續翻頁透過 `postMessage` 切換內部 slide，**不重新加載不閃爍**。兩視窗透過 `BroadcastChannel` 雙向同步。

## 注意事項

- **觀眾永遠看不到 `.notes` 內容** — CSS 預設 `display:none`，只在演講者視圖裡可見
- **別把只給自己看的話寫在 slide 本體上** — 所有提詞必須在 `<aside class="notes">` 裡
- **雙螢幕演講**：打開 `index.html` 按 S 彈出演講者視窗，把觀眾視窗拖到投影/外接螢幕 F 全螢幕，演講者視窗留在自己螢幕
