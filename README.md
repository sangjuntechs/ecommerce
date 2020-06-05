# ecommerce
장고를 통해 ecommerce의 기본 기능을 빌드하는 프로젝트


## `2020/05/28`

상품, 사용자, 주문 모델 db 생성 및 migration 완료
ecommerce settings.py에 앱 등록 완료

#### user
```ts
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
#### product
```ts
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
#### order
```ts
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

admin 사이트 빌드

register 폼 및 path 연결

#### 폼
```ts
from django import forms

class RegisterForm(forms.Form):
    email = forms.EmailField(
        error_messages={
            'required' : '이메일을 입력해주세요.'
        },
        max_length= 64, label='이메일'
    )
    password = forms.CharField(
        error_messages={
            'required' : '비밀번호를 입력해주세요'
        },
        widget=forms.PasswordInput, label='비밀번호'
    )
    re_password = forms.CharField(
        error_messages={
            'required' : '비밀번호를 입력해주세요'
        },
        widget=forms.PasswordInput, label='비밀번호 확인'
    )
```

#### url 연결
```ts
path('register/', RegisterView.as_view())
```

#### 폼을 이용해 register.html 에 폼 형식 전달 후 검증로직 생성
#### register 페이지를 통해 정보 저장
```ts
def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        re_password = cleaned_data.get('re_password')

        if password and re_password:
            if password != re_password:
                self.add_error('password','비밀번호가 일치하지 않습니다.')
                self.add_error('re_password', '비밀번호가 일치하지 않습니다.')
            else:
                user = User(
                    email= email,
                    password= password
                )
                user.save()
```
로그인 html 생성 및 로직 빌드

#### 로그인 폼
```ts
class LoginForm(forms.Form):
    email = forms.EmailField(
        error_messages={
            'required' : '이메일을 입력해주세요.'
        },
        max_length= 64, label='이메일'
    )
    password = forms.CharField(
        error_messages={
            'required' : '비밀번호를 입력해주세요'
        },
        widget=forms.PasswordInput, label='비밀번호'
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                self.add_error('username', '아이디가 존재하지 않습니다.')
                return

            if not check_password(password, user.password):
                self.add_error('password', '비밀번호가 틀렸습니다.')
            else:
                self.user_id = user.id
```

#### 로그인 뷰
```ts
class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'
```

데이터베이스에 존재하는 useremail과 register에서 email이 중복될 시 예외처리 필요.
static login.css 추가해서 로그인 회원가입 페이지 간단하게 리팩토링

#### 프로덕트 뷰 생성
```ts
from django.shortcuts import render
from django.views.generic import ListView
from .models import Product

class ProductList(ListView):
    model = Product
    template_name = 'product.html'
```

#### 프로덕트 폼 생성

```ts
from django import forms
from .models import Product

class RegisterForm(forms.Form):
    name = forms.CharField(
        error_messages={
            'required': '상품명을 입력해주세요.'
        },
        max_length=64, label='상품명'
    )
    price = forms.IntegerField(
        error_messages={
            'required': '가격을 입력해주세요.'
        },
         label='가격'
    )
    description = forms.CharField(
        error_messages={
            'required': '설명을 입력해주세요.'
        },
        label='제품설명'
    )
    stuck = forms.IntegerField(
        error_messages={
            'required': '재고를 입력해주세요'
        },
        label='재고'
    )
```

productRegister 생성

전체적인 레이아웃 css 수정 및 ui 수정
모델 데이터베이스 저장 및 admin 정상작동 확인
로그인 회원가입 상품등록 및 출력 확인
settings.py 타임존 아시아로 변경 완료

#### 프로덕트 디테일

```ts
class ProductDetail(DetailView):
    template_name = 'product_detail.html'
    queryset = Product.objects.all()
    context_object_name = 'product'
```
url 연결
pk를 이용해 제품별 세부페이지 생성 및 링크연결


#### 오더 뷰
```ts
class OrderCreate(FormView):
    form_class = RegisterForm
    success_url = '/product/'

    def form_invalid(self, form):
        return redirect('/product/' + str(form.product))


    def get_form_kwargs(self, **kwargs):
        kw = super().get_form_kwargs(**kwargs)
        kw.update({
            'request': self.request
        })
        return kw
```

세션에 따른 처리 오더 폼

```ts
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
            order = Order(
                quantity = quantity,
                product = Product.objects.get(pk=product),
                user = User.objects.get(email = user)
            )
            order.save()
        else:
            self.product = product
            self.add_error('quantity', '수량을 입력하세요.')
            self.add_error('product', '값이 없습니다.')
```

django.db transaction 을 활용한 재고관리

```ts
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
```

#### 주문 리스트 뷰 

```ts
class OrderList(ListView):
    template_name = 'order.html'
    context_object_name = 'order_list'

    def get_queryset(self, **kwargs):
        queryset = Order.objects.filter(user__email = self.request.session.get('user'))
        return queryset
```

#### 세션에 따른 정보 필터

```ts
def get_queryset(self, **kwargs):
        queryset = Order.objects.filter(user__email = self.request.session.get('user'))
        return queryset
```

#### 데코레이터를 사용한 유저에 대한 세션이 없으면 주문리스트 -> 로그인 리다이렉트

```ts
from django.shortcuts import redirect

def login_required(function):
    def wrap(request, *args, **kwargs):
        user = request.session.get('user')
        if user is None or not user :
            return redirect ('/login')
        return function(request, *args, **kwargs)

    return wrap
```

로그아웃 url 추가

#### 유저레벨 admin, user models 생성 및 admin_required decorator 생성 권한 설정 ProductCreate에 @method_decorator

```ts
def admin_required(function):
    def wrap(request, *args, **kwargs):
        user = request.session.get('user')
        if user is None or not user :
            return redirect ('/login')

        user = User.objects.get(email=user)
        if user.level != 'admin':
            return redirect ('/')


        return function(request, *args, **kwargs)

    return wrap
```

브랜치 desk1 index, loginsuccess화면 구분 및 css작업