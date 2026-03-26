from django.shortcuts import render, redirect
from django.db import transaction
from .models import Order, OrderItem
from goods.models import Product
from .tasks import send_order_email

def checkout(request):
    """結帳與產生訂單邏輯"""
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart_detail') # 購物車空的就踢回去
        
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        
        try:
            # 🔹 關鍵技術：開啟資料庫事務 (Transaction)
            # 這裡面的操作要嘛「全部成功」，要嘛「全部失敗(Rollback)」
            with transaction.atomic():
                # 1. 建立訂單主表 (總金額先設為0，等一下算)
                order = Order.objects.create(
                    name=name, phone=phone, address=address, total_amount=0
                )
                
                total_amount = 0
                
                # 2. 處理購物車裡的每一個商品
                for product_id_str, quantity in cart.items():
                    # 🔥 面試必考：悲觀鎖 select_for_update()
                    # 告訴 MySQL：「我要處理這個商品，別的訂單先排隊等我處理完！」
                    product = Product.objects.select_for_update().get(id=int(product_id_str))
                    
                    # 3. 檢查庫存夠不夠
                    if product.stock < quantity:
                        raise ValueError(f"抱歉，【{product.name}】 庫存不足！剩下 {product.stock} 件。")
                        
                    # 4. 扣除庫存並存檔
                    product.stock -= quantity
                    product.save()
                    
                    # 5. 計算金額並建立訂單明細
                    price = product.price
                    subtotal = price * quantity
                    total_amount += subtotal
                    
                    OrderItem.objects.create(
                        order=order, product=product, price=price, quantity=quantity
                    )
                
                # 6. 更新訂單總金額
                order.total_amount = total_amount
                order.save()
                
                # 7. 結帳成功，清空購物車
                request.session['cart'] = {}
                request.session.modified = True
                
                # 🔹 核心魔法：使用 .delay() 非同步觸發任務！
                # 這樣程式就不會在這裡等 5 秒，而是瞬間跳到下一行
                send_order_email.delay(order.id, order.phone)
                
                # 導向成功畫面
                return render(request, 'orders/success.html', {'order': order})
                
        except ValueError as e:
            # 如果發生庫存不足，資料庫不會扣款也不會建訂單，直接退回並顯示錯誤
            return render(request, 'orders/checkout.html', {'error': str(e)})
            
    # 如果是 GET 請求，顯示填寫資料的表單
    return render(request, 'orders/checkout.html')


def order_search(request):
    """透過電話號碼查詢訂單"""
    orders = []
    # 嘗試從網址參數 (GET 請求) 中獲取 'phone'
    phone = request.GET.get('phone', '')
    
    if phone:
        # 如果有輸入電話，就去資料庫把這個人的訂單都撈出來
        # 並且使用 prefetch_related 把訂單明細也一併撈出來 (優化資料庫查詢效能)
        orders = Order.objects.filter(phone=phone).prefetch_related('items__product').order_by('-created_at')
        
    return render(request, 'orders/search.html', {
        'orders': orders, 
        'phone': phone
    })
