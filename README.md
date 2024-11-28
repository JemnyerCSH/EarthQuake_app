# 地震應急互動系統 Earthquake Emergency Interaction System

## 簡介
這是一個模擬地震應急情境的互動系統，通過文字遊戲與地震知識問答的方式，幫助用戶提升地震應急的準備與應對能力。本系統結合 Flask 框架與 AI 模型（如 TAIDE），提供即時互動與知識學習，適合教育、培訓及應急演練等場景。

## 功能特點
1. **地震通知**：實時從地震數據源獲取最新的地震資訊，顯示在用戶界面中。
2. **模擬問答遊戲**：通過地震情境模擬題目，引導用戶學習正確的應對行動。
3. **AI 助手互動**：基於自然語言生成模型的 AI 助手，回答用戶關於地震相關問題並提供專業建議。
4. **情境模擬**：根據實際地震場景設計長情境題，幫助用戶進行深入的應急演練。

## 技術細節
- **後端框架**：使用 Flask 實現 API 路由與伺服器邏輯。
- **前端**：使用 HTML、CSS 與 JavaScript 提供簡單直觀的用戶界面。
- **AI 模型**：使用 Hugging Face 的 `transformers` 庫載入 TAIDE 模型，實現自然語言生成功能。
- **地震數據來源**：從 USGS (美國地質調查局) 獲取地震事件的公開數據。
- **問答題庫**：包含多達 38 道地震應急相關的模擬題，涵蓋各種場景。

## 目錄結構
	```bash
	Earthquake_app/
	├── app.py                # 主程式文件，包含伺服器邏輯
	├── templates/
	│   └── index.html        # 前端主頁
	├── static/
	│   ├── style.css/        # CSS 樣式文件
	│   ├── script.js/        # JavaScript 文件
	├── questions.py          # 問答題庫文件
	├── requirements.txt      # 依賴包清單
 	├── .gitignore
	└── README.md             # 專案說明文件

## 使用方法
### 環境設置
1. 安裝必要的 Python 依賴包：
   ```bash
   pip install -r requirements.txt
2. 確保您已安裝 Python 3.8+ 並設定 Hugging Face 模型所需的環境。
3. 確保您已經有取得 Hugging Face 所需的 Token，並將它設定成變數名稱 HF_TOKEN。（可以開啟一個.env檔保存您的 TOKEN，這樣可以有效的提高隱私性）

### 啟動伺服器
1. 啟動 Flask 伺服器：
   ```bash
   python app.py
2. 打開瀏覽器並訪問 http://127.0.0.1:5001 查看系統。

## 注意事項
- 本專案為學術研究及教育用途，不可用於實際地震應急決策。
- 問答內容來源於地震安全相關資料，建議定期更新以確保準確性。

## 未來規劃
- 增加多語言支持，覆蓋更多國家和地區。
- 提供地震知識的詳細解析，提升學習效果。
- 優化 AI 助手的回應速度與準確度。

## 貢獻指南
如果您對本專案有改進建議或想要提供更多地震情境題，歡迎提交 Pull Request 或聯繫我。

## 聯絡方式
- 作者: JemnyerCSH
- Email: siewhsuan@nlp.csie.ntust.edu.tw
- GitHub Repo: https://github.com/JemnyerCSH/EarthQuake_app

