from django.db import models

# ---------------------------------------------------------
# Category (商品分類)
# ---------------------------------------------------------
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="分類名稱")
    # slug 用於網址，例如 /category/electronic-devices/
    slug = models.SlugField(unique=True, verbose_name="網址別名")

    class Meta:
        verbose_name = "商品分類"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# ---------------------------------------------------------
# Product (商品主表)
# ---------------------------------------------------------
class Product(models.Model):
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='products',
        verbose_name="所屬分類"
    )
    name = models.CharField(max_length=200, verbose_name="商品名稱")
    description = models.TextField(verbose_name="商品描述", blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="價格")
    stock = models.IntegerField(default=0, verbose_name="庫存數量")
    # 先用 URL 代表圖片，Day 4 我們再來處理實體圖片上傳
    #image_url = models.URLField(max_length=500, blank=True, verbose_name="圖片連結")
    image = models.ImageField(upload_to='products/', verbose_name="商品圖片", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="上架時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="最後更新")

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = verbose_name
        ordering = ('-created_at',)

    def __str__(self):
        return self.name