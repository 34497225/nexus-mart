from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# 使用 @admin.register 裝飾器註冊 User 模型
@admin.register(User)
class MyUserAdmin(UserAdmin):
    """
    擴展 Django 內建的 UserAdmin。
    如果不這樣寫，新增的 mobile 欄位在後台會看不到。
    """
    # 1. 在列表頁面顯示手機號碼
    list_display = ('username', 'email', 'mobile', 'is_staff')
    
    # 2. 在編輯頁面增加一個「額外資訊」區塊來顯示手機號碼
    fieldsets = UserAdmin.fieldsets + (
        ('額外資訊', {'fields': ('mobile',)}),
    )
    
    # 3. 註冊時也允許輸入手機號碼 (選配)
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('額外資訊', {'fields': ('mobile',)}),
    )