from django.shortcuts import render, get_object_or_404
from .models import Product

def index(request):
    """商城首頁視圖"""
    # 抓取所有商品，並按造建立時間倒序排列
    products = Product.objects.all().order_by('-created_at')
    
    # 將資料傳遞給模板
    return render(request, 'goods/index.html', {'products': products})

def detail(request, product_id):
    """單一商品詳情視圖"""
    # 根據網址傳來的 product_id 去資料庫找商品
    # 如果找不到（例如輸入了不存在的 ID），會自動報錯 404 (找不到網頁)
    product = get_object_or_404(Product, id=product_id)
    
    return render(request, 'goods/detail.html', {'product': product})
