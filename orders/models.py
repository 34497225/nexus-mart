from django.db import models
# 必須引入 goods 裡的 Product，因為訂單明細需要關聯到商品
from goods.models import Product

class Order(models.Model):
    """訂單主表"""
    name = models.CharField(max_length=50, verbose_name="收件人姓名")
    phone = models.CharField(max_length=20, verbose_name="聯絡電話")
    address = models.TextField(verbose_name="收件地址")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="總金額")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")

    # 🔹 加上這段 class Meta，後台就會顯示漂亮的中文「訂單」
    class Meta:
        verbose_name = "訂單"
        verbose_name_plural = "訂單"

    def __str__(self):
        return f"訂單編號 #{self.id} - {self.name}"

class OrderItem(models.Model):
    """訂單明細表"""
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="商品")
    price = models.IntegerField(verbose_name="購買單價")
    quantity = models.IntegerField(verbose_name="購買數量")

    # 🔹 加上這段 class Meta，後台就會顯示漂亮的中文「訂單明細」
    class Meta:
        verbose_name = "訂單明細"
        verbose_name_plural = "訂單明細"

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"