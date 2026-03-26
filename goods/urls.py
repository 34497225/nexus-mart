from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # 首頁路徑
    
    path('search/', views.search, name='search'), # 🔹 新增這行：搜尋專用路由
    
    # 🔹 新增：動態路由。<int:product_id> 代表抓取網址中的整數
    path('<int:product_id>/', views.detail, name='detail'),
]
