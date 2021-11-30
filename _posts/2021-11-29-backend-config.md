---
layout: single
title:  "MyBistro--BackEnd Configuration"
date:   2021-11-28 21:00:00 +0800
categories: doc
toc: true
toc_label: "Contents"
---


## 後端是以Python 開發的Django Restful API

目前定義的API:    

|Methods |Urls|Actions|
|-----|-----------|-----------------|
|POST|api/token/obtain/|login and get a JWT token<br>登入並取得JWT Token|
|POST|api/token/refresh/|reflesh JWT token<br>更新JWT Token|
|POST|api/signup/|create a user<br>註册新使用者|
|POST|api/logout/|user logout<br>使用者登出|
|GET|api/bistro/user/|get the current login user<br>取得目前登入的使用者資訊|
|GET|api/bistro/test/|test api|
|GET|api/bistro/menus/|get BistroMenus list<br>取得餐酒館系統的菜單|
|GET|api/bistro/menus/:pk|get BistroMenus by pk(id)<br>取得餐酒館系統的菜單 by pk|

### 初使開發環境
先設定一個Python的虛擬環境，再啟始一個新的Django專案。  
使用Python的套件管理工具:pipenv，  
是一種CLI,要在命令列執行，請先安裝 ,指令: `$>pip3 install pipenv`  
新增工作目錄:ex:D:\Projects\django\bistro_env
``` terminal
$>cd D:\Projects\django\bistro_env
$>pipenv install django
```
就可以創建Python專案的初使開發環境。    
安裝時建立虛擬環境，一般會安裝到類似以下路徑 :   
C:\Users\yourname\.virtualenvs\bistro_env-28SDm1U8

#### 創建Django專案    
``` terminal    
$>pip shell   (進入shell)   
(bistro_env-28SDm1U8)>django-admin startproject bistro_backend .
```
(.代表目前目錄當根目錄，才不會又多一層目錄)      
django-admin工具會創建如下所示的文件夾結構    
``` terminal   
bistro_env/
    manage.py
    bistro_backend/
        __init__.py
        settings.py
        urls.py
        wsgi.py
```

#### 起動Django專案    
``` terminal    
(bistro_env-28SDm1U8)>python manage.py runserver
```
打開:[http://127.0.0.1:8000](http://127.0.0.1:8000){:target="_blank"} 檢查是否安裝完成

#### 新增Django專案的App 
指令:  
``` terminal    
(bistro_env-28SDm1U8)>python manage.py startapp accounts
(bistro_env-28SDm1U8)>python manage.py startapp bistro
```
accounts:負責處理登入系統的使用者API  
bistro:負責處理系統的業務API  
修改/bistro_backend/settings.py  
``` python
...
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'bistro',
]

LANGUAGE_CODE= 'zh-hant'
 
TIME_ZONE = 'Asia/Taipei'

```

#### 設定VisualStudio Code  
1. 使用虛擬環境的python直譯器  
In VSCode->command palette->python interpreter  
Chose  C:\Users\vincent\.virtualenvs\bistro_env-28SDm1U8\Scripts\python.exe  
2. 修改.vscode->setting.json  
加入一行:  
```
{"terminal.integrated.shellArgs.windows": ["-ExecutionPolicy", "Bypass"]}
```

#### 快速安裝所有需要的套件  
修改Pipfile檔內所需要相依的packages 
``` terminal   
[packages]
django = "*"
django-cors-headers = "*"
pymango = "*"
mongoengine = "*"
django-rest-framework-mongoengine = "*"
djangorestframework-simplejwt-mongoengine = "*"
blinker = "*"
bcrypt = "*"
python-decouple = "*"
```     
指令:    
``` terminal    
(bistro_env-28SDm1U8)>pipenv install
```

### 設定資料庫連線
Django有三種方法可以連接MongoDB  
1. PyMongo 是MongoDB提供,用Python寫的driver,也是MongoDB推薦的driver。  
2. Djongo 好處是可以繼續使用Djanogo內建的特色功能，像是django.db.models ,ORM等，感覺像在用SQL類的資料庫，所以也需要`run>  python manage.py makemigrations` and  `python manage.py migrate` 。  其實作方法是將SQL轉為PyMongo語法，所以功能會受限。我之前[上一版tag:conntype1](https://github.com/vuzzil/mybistro/tags){:target="_blank"} 就是採用Djongo實作。
3. MongoEngine 其底層也是用PyMongo寫的，好處ORM可以用MongoDB的特色功能,如Document,也可以和PyMongo混用。
但就不能用Djanogo內建的Admin和Models,所以要自己實作Customize User(ex:[BistroUser](https://github.com/vuzzil/mybistro/blob/master/accounts/models.py){:target="_blank"})。  

#### 安裝資料庫連線driver  
``` terminal    
(bistro_env-28SDm1U8)>pipenv install pymango
(bistro_env-28SDm1U8)>pipenv install mongoengine
```
修改/bistro_backend/settings.py  
``` python
...
INSTALLED_APPS = [
    ...
    pymango,
    django_mongoengine,
    ...
]    

MONGODB_DATABASES = {
    "default": {
        "name": 'bistrodb',
        "db": 'bistrodb',
        "username": "db_username",
        "password": "db_password",
        "host": "localhost",
        "port": 27017,
        "authentication_source": "bistrodb",
        "authentication_mechanism": "SCRAM-SHA-256",
        "tz_aware": True,  # if you using timezones in django (USE_TZ = True)
    },
}
MONGOENGINE_USER_DOCUMENT = 'accounts.models.BistroUser'
SESSION_ENGINE = 'django_mongoengine.sessions'
SESSION_SERIALIZER = 'django_mongoengine.sessions.BSONSerializer'

```

### 整合rest-framework

#### 安裝需要的套件:
一般是安裝 djangorestframework，但因還要搭配MongoDB    
所以安裝[django-rest-framework-mongoengine](https://github.com/umutbozkurt/django-rest-framework-mongoengine){:target="_blank"} 即可。
``` terminal
$>pipenv install django-rest-framework-mongoengine
```
修改/bistro_backend/settings.py  
``` python
...
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework_mongoengine',
]

```


#### 整合方法:
##### 定義Api URL
ex: /bistro_backend/accounts/urls.py  
``` python
from django.urls import path
from accounts import views
...
urlpatterns = [
    ...
    path('api/signup/', views.bistrouser_create, name="create_user"),
    path('api/logout/', views.bistrouser_logout, name="logout_user"),
    path('api/bistro/user/', views.bistrouser_detail, name="get_user"),
]
...
```
修改/bistro_backend/urls.py
``` python
from django.urls import include

urlpatterns = [
    ...
    url(r'^', include('accounts.urls')),
    ...
]
```

##### View 實作Api  
rest_framework 用 @api_view decorator 宣告Api  
ex: /bistro_backend/accounts/views.py  
``` python
from rest_framework.decorators import api_view
...
@api_view(['POST'])
def bistrouser_create(request):
    serializer = BistroUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        if user:
            json = serializer.data
            return Response(json, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
...
```

##### Model 改繼承mongoengine.Document  
ex: /bistro_backend/accounts/models.py  
``` python
from mongoengine import Document, EmailField, StringField, BooleanField, DateTimeField
...

class BistroUser(Document):
    """
    Customize Bistro  user 
    """
    email = EmailField(verbose_name='email address', max_length=255, unique=True)
    username = StringField(verbose_name='username', blank=False, max_length=150)
    password = StringField(verbose_name='password', blank=False, max_length=128)
    theme = StringField(blank=True, max_length=20)
    staff = BooleanField(blank=False, default=False)  # a admin user; non super-user
    admin = BooleanField(blank=False, default=False)  # a superuser
    date_joined = DateTimeField(default=datetime.now(), verbose_name='date joined')
    last_login = DateTimeField(blank=True, verbose_name='last login')
    is_authenticated = BooleanField(blank=False, default=False)

```
##### Serializer 改繼承rest_framework_mongoengine.serializers.DocumentSerializer 
ex: /bistro_backend/accounts/serializers.py  
``` python
from rest_framework_mongoengine import serializers
...
class BistroUserSerializer(serializers.DocumentSerializer):
    """
    For login/signup use
    """
    class Meta:
        model = BistroUser
        fields = '__all__'
    ...
```

### 整合JWT Authenticatioon

#### 安裝需要的套件
一般是安裝 djangorestframework_simplejwt，  
但因還要搭配mongoengine，所以要安裝[mongoengine版 simplejwt](https://djangorestframework-simplejwt-mongoengine.readthedocs.io/en/latest/getting_started.html){:target="_blank"}   
``` terminal
$>pipenv install djangorestframework-simplejwt-mongoengine
```
#### 整合方法:
修改/bistro_backend/settings.py  
將設定API預設的權限=IsAuthenticated,代表存取Api需要先通過登入驗證。  
目前設定access token有效時限=5分鐘,逾時需以reflesh token來更新access token,
reflesh token有效時限=14天,但若使用者登出，則reflesh token會加入BlackList而失效，就要重新登入。  
Note:BlackList資料會一直成長，可以利用blacklist app提供的管理指令:&gt;python manage.py flushexpiredtokens，
用排程程式(ex:cron)每天清除已經逾期的資料。  
``` python
from datetime import timedelta
...
INSTALLED_APPS = [
    ...
    'rest_framework_simplejwt_mongoengine',
    'rest_framework_simplejwt_mongoengine.token_blacklist',
]
...
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt_mongoengine.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT_MONGOENGINE = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=14),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('JWT',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'TOKEN_USER_CLASS': ('rest_framework_simplejwt_mongoengine.models.TokenUser',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt_mongoengine.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

```
修改/bistro_backend/accounts/urls.py  
``` python
from rest_framework_simplejwt_mongoengine import views as jwt_views
from rest_framework_simplejwt_mongoengine.views import TokenObtainPairView
...
urlpatterns = [
    ...
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/obtain/', views.ObtainTokenPairWithThemeView.as_view(), name='token_create'),  # ==login
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
...
```
但login/signup需要開放權限:permissions.AllowAny  
修改/bistro_backend/accounts/views.py  
``` python
class ObtainTokenPairWithThemeView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = BistroTokenObtainPairSerializer



@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def bistrouser_create(request):
...
```
#### 自訂Django登入的驗證方式
改以email/password驗證  
新增/bistro_backend/accounts/auth.py  
``` python
from django.contrib.auth.backends import BaseBackend
from datetime import datetime
from .models import BistroUser

class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = BistroUser
        
        try:
            if email==None:
                email = kwargs.get('username')              #Django Admin Page:use username field
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                user.last_login = datetime.now()
                user.is_authenticated = True
                user.save()
                #print('user saved:' + str(user))

                return user
        return None

    def get_user(self, user_id):
        UserModel = BistroUser
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

```

修改/bistro_backend/settings.py  
``` python
...
AUTHENTICATION_BACKENDS = [
    'accounts.auth.EmailBackend',
]
...
```
##### 使用bcrypt加密/驗證password
實作BistroUser.check_password  
安裝需要的套件  
``` terminal
$>pipenv install blinker
$>pipenv install bcrypt
```
修改/bistro_backend/accounts/models.py  
``` python
from bcrypt import checkpw
...
class BistroUser(Document):
    ...
    def check_password(self, password):
        return checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
```
新増登入的使用者時，存資料庫前要加密password  
修改/bistro_backend/accounts/serializers.py  
``` python
from bcrypt import hashpw, gensalt
...
class BistroUserSerializer(serializers.DocumentSerializer):
    ...
    def create(self, validated_data):
        ...
        #encode password
        hashed = hashpw(user.password.encode('utf8'), gensalt())
        user.password = hashed.decode('utf8')
        
        user.save()

```


### 分離設定檔敏感資料
using python-decouple  
``` terminal
$>pipenv install python-decouple
```
新增 .env檔 到專案根目錄   
將敏感資料存放此處:  
```
SECRET_KEY = 'django-insecure-atvkjkx0z1xic5a69%m$h6mi9m1n+)_b+qs(4q63w_u!c)#%45'

DATABASE_HOST = 'localhost'
DATABASE_PORT = '27017'
DATABASE_USERNAME = 'db_username'
DATABASE_PASSWORD = 'db_password'
```  
修改.gitignore檔, add:  
```
.env
```
修改/bistro_backend/settings.py  
``` python
from decouple import config
…
SECRET_KEY = config("SECRET_KEY")

MONGODB_DATABASES = {
    "default": {
        "name": 'bistrodb',
        "db": 'bistrodb',
        "username": config("DATABASE_USERNAME"),
        "password": config("DATABASE_PASSWORD"),
        "host": config("DATABASE_HOST", default='localhost'),
        "port": config("DATABASE_PORT", default=27017, cast=int),
        "authentication_source": "bistrodb",
        "authentication_mechanism": "SCRAM-SHA-256",
        "tz_aware": True,  # if you using timezones in django (USE_TZ = True)
    },
}
```

### 設定跨來源資源共用（CORS）
修改/bistro_backend/settings.py  
``` python
...
# CORS
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',  # for local react app use
    'http://localhost:8080',  # for local nginx use
)
```


