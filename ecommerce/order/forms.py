from django import forms
from .models import Order
from product.models import Product
from user.models import User
from django.db import  transaction

class RegisterForm(forms.Form):
    
    def __init__ (self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
      
    
    quantity = forms.IntegerField(
        error_messages={
            'required': '상품의 개수를 입력하세요.'
        },
        label='수량'
    )

    product = forms.IntegerField(
        error_messages={
            'required': '설명을 입력해주세요.'
        },
        label='제품설명', widget=forms.HiddenInput
        )
   


    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        product = cleaned_data.get('product')
        user = self.request.session.get('user')

        if quantity and product and user:
            with transaction.atomic():
                prod = Product.objects.get(pk=product)
                order = Order(
                    quantity = quantity,
                    product = prod,
                    user = User.objects.get(email = user)
                )
                order.save()
                prod.stuck -= quantity
                prod.save()
        else:
            self.product = product
            self.add_error('quantity', '수량을 입력하세요.')
            self.add_error('product', '값이 없습니다.')
            
        

        