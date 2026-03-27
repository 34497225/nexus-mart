from django.shortcuts import render, get_object_or_404
from .models import Product
from django.db.models import Q

def index(request):
    """商城首頁視圖"""
    # 🔹 加上 .filter(is_active=True)，只抓取有上架的商品
    products = Product.objects.filter(is_active=True).order_by('-created_at')
    
    # 將資料傳遞給模板
    return render(request, 'goods/index.html', {'products': products})

def detail(request, product_id):
    """單一商品詳情視圖"""
    # 根據網址傳來的 product_id 去資料庫找商品
    # 如果找不到（例如輸入了不存在的 ID），會自動報錯 404 (找不到網頁)
    product = get_object_or_404(Product, id=product_id)
    
    return render(request, 'goods/detail.html', {'product': product})

def search(request):
    """關鍵字搜尋商品邏輯"""
    # 取得網址列的 q 參數，例如 /search/?q=西瓜
    query = request.GET.get('q', '').strip()
    
    if query:
        # 🔹 同樣加上 is_active=True 的過濾條件
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query),
            is_active=True
        ).order_by('-created_at')
    else:
        # 如果沒輸入關鍵字，回傳空清單
        products = Product.objects.none()
        
    return render(request, 'goods/search.html', {
        'products': products,
        'query': query
    })
