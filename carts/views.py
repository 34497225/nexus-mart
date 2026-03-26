from django.shortcuts import render, redirect, get_object_or_404
from goods.models import Product

def add_cart(request, product_id):
    """加入購物車邏輯"""
    # 1. 確保是 POST 請求 (安全機制)
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        # 從表單抓取數量，預設為 1
        quantity = int(request.POST.get('quantity', 1))
        
        # 2. 從 Session 取出購物車，如果沒有就建一個空的字典
        cart = request.session.get('cart', {})
        product_id_str = str(product.id) # Session 的 key 必須是字串
        
        # 3. 如果商品已經在車裡，數量增加；否則新增進去
        if product_id_str in cart:
            cart[product_id_str] += quantity
        else:
            cart[product_id_str] = quantity
            
        # 4. 把更新後的購物車存回 Session
        request.session['cart'] = cart
        request.session.modified = True # 告訴 Django Session 被修改了
        
    # 加入後，重新導向到查看購物車頁面
    return redirect('cart_detail')


def cart_detail(request):
    """查看購物車頁面"""
    cart = request.session.get('cart', {})
    
    cart_items = []
    total_price = 0
    
    # 把 Session 裡的 ID 轉換成真實的商品物件，並計算小計
    for product_id_str, quantity in cart.items():
        product = Product.objects.get(id=int(product_id_str))
        subtotal = product.price * quantity
        total_price += subtotal
        
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })
        
    return render(request, 'carts/detail.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })