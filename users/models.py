from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # 增加手機號碼欄位 (可為空)
    mobile = models.CharField(max_length=11, unique=True, verbose_name="手機號碼", null=True, blank=True)
    
    class Meta:
        verbose_name = "用戶"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username