from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('search/', views.order_search, name='order_search'), # 🔹 新增這行查詢路由
]