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

#### 新增Django專案App 
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
Model 改繼承mongoengine.Document  
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
Serializer 改繼承rest_framework_mongoengine.serializers.DocumentSerializer  
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




