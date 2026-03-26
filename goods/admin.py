from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    # 自動根據名稱生成 slug
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'created_at')
    list_filter = ('category', 'created_at')
    # 讓後端介面可以直接搜尋商品名稱
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock') # 可以在清單直接修改價格與庫存