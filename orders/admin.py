from django.contrib import admin
from .models import Order, OrderItem

# 1. 建立「訂單明細」的內聯顯示 (Inline)
# 這樣可以在查看「訂單」時，直接在同一頁面看到裡面包含的「商品明細」
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # 預設不顯示多餘的空白列
    
    # 為了保護歷史訂單不被隨意竄改，我們通常會把明細設為唯讀
    # 如果你希望在後台可以修改客人買的數量，可以把這行註解掉
    readonly_fields = ('product', 'price', 'quantity')

# 2. 註冊「訂單」模型
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # 列表頁要顯示的欄位
    list_display = ('id', 'name', 'phone', 'total_amount', 'created_at')
    
    # 右側篩選器 (可以用下單時間來篩選)
    list_filter = ('created_at',)
    
    # 搜尋框 (可以用客人的名字或電話來搜尋訂單)
    search_fields = ('name', 'phone')
    
    # 把剛剛寫好的「訂單明細」掛載進來
    inlines = [OrderItemInline]
    
    # 預設照時間倒序排列 (最新的訂單在最上面)
    ordering = ('-created_at',)