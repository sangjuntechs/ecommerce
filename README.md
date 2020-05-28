# ecommerce
장고를 통해 ecommerce의 기본 기능을 빌드하는 프로젝트


## `2020/05/28`

상품, 사용자, 주문 모델 db 생성 및 migration 완료
ecommerce settings.py에 앱 등록 완료

user
```
from django.db import models

class user(models.Model):
    email = models.EmailField(verbose_name='이메일')
    password = models.CharField(max_length=64, verbose_name='비밀번호')
    register_date = models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')

    class Meta:
        db_table = 'ecommerce_user'
        verbose_name = '사용자'
        verbose_name_plural = '사용자'
```
product
```
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=256, verbose_name='상품명')
    price = models.IntegerField(verbose_name='상품가격')
    description = models.TextField(verbose_name='설명')
    stuck = models.IntegerField(verbose_name='재고')
    register_date = models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')

    class Meta:
        db_table = 'ecommerce_product'
        verbose_name = '상품'
        verbose_name_plural = '상품'
```
order
```
from django.db import models

class Order(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name="사용자")
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, verbose_name='상품')
    quantity = models.IntegerField(verbose_name='수량')
    register_date = models.DateTimeField(auto_now_add=True, verbose_name='등록 날짜')

    class Meta:
        db_table = 'ecommerce_order'
        verbose_name = '주문'
        verbose_name_plural = '주문'
```