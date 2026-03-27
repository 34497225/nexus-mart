🛒 NexusMart 企業級全端電商與自動化維運專案

這是一個基於 Django + MySQL + Redis 構建的現代化全端電商平台，並具備完整的 CI/CD 自動化部署與雲端監控系統。專案旨在展示如何將企業級業務邏輯與現代 DevOps 流程完美結合。

🌐 線上展示與系統監控

🛍️ 商城入口 (Live Demo): http://43.212.25.222:8002

📊 系統實時狀態 (Status Page): http://43.212.25.222:3001
(註：為節省雲端資源，若連線失敗可能為主機休眠狀態)

🛠️ 技術棧 (Tech Stack)

    後端與資料庫 (Backend & Data)

    核心框架: Django 4.2 (Python 3.9+)

    關聯式資料庫: MySQL 8.0 (處理訂單與商品關聯)

    快取與訊息佇列: Redis 7.0 (購物車系統、任務 Broker)

    非同步任務: Celery 5.3 (背景處理耗時任務)

    維運與部署 (DevOps & Infrastructure)

    網頁伺服器雙引擎: Nginx (反向代理與靜態資源) + Gunicorn (WSGI)

    容器化技術: Docker & Docker Compose

    雲端基礎設施: AWS EC2 (t3.micro, 配置 2GB Swap 優化記憶體)

    自動化流水線: GitHub Actions (CI/CD)

    可觀測性: Uptime Kuma (24/7 服務健康監控)

🏗️ 系統架構圖 (Architecture Diagram)

    [使用者] -> [AWS 防火牆 (Port 8002)] -> [Nginx 反向代理]
                                            |
            +---------------------------------+---------------------------------+
            |                                 |                                 |
    [靜態檔案 (CSS/Images)]           [Gunicorn App Server]             [Uptime Kuma 監控]
                                            |
            +---------------------------------+---------------------------------+
            |                                 |                                 |
    [MySQL 8.0 資料庫]                 [Redis 緩存/任務佇列]             [Celery 背景機器人]


🚀 核心專案亮點 (Project Highlights)

1. 併發處理與防超賣機制 (Concurrency Control)

    痛點：電商促銷時，多位使用者同時下單容易導致庫存為負的「超賣」問題。

    解決方案：在訂單結帳的 Transaction（事務）中，精準使用 MySQL 悲觀鎖 (select_for_update)，確保高併發情境下的庫存扣減具有絕對的原子性與一致性。

2. 非同步解耦架構 (Asynchronous Task Queue)

    痛點：訂單成立後發送 Email 或簡訊等 I/O 密集型操作，會導致 API 回應時間過長，造成網頁卡頓。

    解決方案：導入 Celery + Redis 架構，將耗時任務丟入背景 Worker 處理，確保結帳 API 保持毫秒級別的回應速度 (Latency)。

3. 生產級 Zero-Touch 自動化部署 (CI/CD)

    自動化：編寫 GitHub Actions 工作流，監聽 main 分支。當代碼 Push 後，自動透過 SSH 觸發 AWS 上的 docker-compose up --build -d 進行滾動更新。

    安全性加固：遵循 Secrets Separation 原則，將資料庫密碼與 Django SECRET_KEY 等敏感資訊存於 GitHub Secrets，於部署時動態注入 .env，確保密鑰不落地且不進 Git 版控。

4. 資源極限優化與排錯實錄 (Ops Troubleshooting)

    記憶體優化 (OOM 防禦)：在僅有 1GB RAM 的 AWS t3.micro 環境中運行 5 個重度容器，曾導致 SSH 崩潰。透過深入 Linux 內核設定，手動掛載 2.0GB Swap 虛擬記憶體，成功穩住系統負載。

    磁碟空間管理：定期執行 Docker Image Prune 與系統日誌壓縮 (journalctl --vacuum-size)，解決 8GB SSD 空間不足導致的 Build Fail 問題。

    協定升級除錯：針對 Django 4.0 的安全更新，動態配置 CSRF_TRUSTED_ORIGINS，完美解決 Nginx 反向代理導致的 403 跨站請求拒絕問題。

⚙️ 快速啟動 (Local Development)

若您想在本地端運行此專案進行測試，請依照以下步驟操作：

1. 取得程式碼

    git clone https://github.com/34497225/nexus-mart.git
    cd nexus-mart


2. 設定環境變數

在專案根目錄建立 .env 檔案，並填入以下內容：

    DEBUG=True
    DATABASE_URL=mysql://root:password@db:3306/nexus_mart
    SECRET_KEY=your_super_secret_key_for_local_dev
    CELERY_BROKER_URL=redis://redis:6379/0


3. 一鍵啟動 (Docker Compose)

    請確保您的電腦已安裝 Docker Desktop。

    # 啟動包含 Django, MySQL, Redis, Celery 的所有服務
    docker compose up --build -d


4. 初始化資料庫與管理員

    # 執行資料庫遷移
    docker compose exec web python manage.py migrate

    # 建立超級管理員 (按提示輸入帳號密碼)
    docker compose exec web python manage.py createsuperuser


👉 現在您可以打開瀏覽器訪問 http://localhost:8001 開始購物了！

👨‍💻 作者 (Author)

smg60214 * GitHub: https://github.com/34497225

專注於後端開發、雲端架構 (AWS) 與 SRE 維運自動化。