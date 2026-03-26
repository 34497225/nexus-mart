from celery import shared_task
import time

@shared_task
def send_order_email(order_id, user_phone):
    """
    模擬發送訂單確認信件的耗時任務
    """
    print(f"========== 開始處理訂單 #{order_id} ==========")
    print(f"正在連線至郵件伺服器...")
    
    # 模擬寄信需要花費 5 秒鐘 (這在網頁上會卡死使用者)
    time.sleep(5)
    
    print(f"✅ 已成功發送簡訊/Email 給 {user_phone}！訂單 #{order_id} 處理完畢。")
    print(f"==============================================")
    
    return f"Order {order_id} email sent."