# 🛒 NexusMart 全端電商實作專案

這是一個基於 Django + MySQL + Redis 構建的現代化全端電商平台。

## 🚀 核心技術與維運亮點
* **後端框架**：Django 4.2 (Python 3.9)
* **資料庫**：MySQL 8.0 (處理訂單與商品關聯)
* **快取與訊息佇列**：Redis (購物車系統、Celery Broker)
* **非同步任務**：Celery (背景處理發信等耗時任務，確保 API 毫秒級回應)
* **防超賣機制**：運用 MySQL 悲觀鎖 (`select_for_update`) 確保高併發下庫存扣減正確
* **維運部署**：使用 Docker 與 Docker Compose 實現跨平台環境一致性
* **前端介面**：Tailwind CSS 結合 Django Templates 實現響應式設計

## 🛠️ 如何在本地運行
1. 確保已安裝 Docker Desktop。
2. Clone 專案後，在根目錄建立 `.env` 檔案並填寫資料庫密碼。
3. 執行 `docker compose up --build -d`。
4. 瀏覽 `http://localhost:8002`。
