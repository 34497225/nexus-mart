from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    # 自動根據名稱生成 slug
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # 1. 決定列表頁要顯示哪些欄位 (把 is_active 加進來)
    list_display = ('id', 'name', 'category', 'price', 'stock', 'is_active', 'created_at')
    
    # 2. 右側的篩選器 (可以用「是否上架」來篩選商品)
    list_filter = ('category', 'is_active', 'created_at')
    
    # 3. ⭐️ 最強大的功能：允許在列表頁直接編輯這些欄位！
    list_editable = ('price', 'stock', 'is_active')
    
    # 4. 搜尋框
    search_fields = ('name', 'description')