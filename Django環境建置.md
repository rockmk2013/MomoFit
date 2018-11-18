# Django 環境建置
## 1. 建立虛擬環境&安裝Django(windows)
### 新建一個資料夾在C槽底下，名為momomywife
```
mkdir momomywife
```
### 在資料夾底下建立虛擬環境
```
python -m venv myvenv
```
### 啟動虛擬環境並安裝Django
```
myvenv\Scripts\activate
pip install django
```

## 2. 建立Django專案及Web app
使用django套件建立新專案，並在mysite底下加入設定檔
```
django-admin.py startproject mysite . 
```
創建完之後，momomywife資料夾下，會有一個manage.py檔以及一個mysite資料夾，mysite資料夾會有一些設定檔。接著我們在專案下新建一個app。
momofit 是指你的app名稱。
```
python manage.py startapp momofit
```

設定好app後，進入mysite底下的settings.py檔案，修改INSTALLED_APPS，加入**momofit.apps.MomofitConfig** 
對應到momofit/apps.py當中的class。

## 3. 設定資料庫

本次專案使用資料庫為mysql，首先須安裝python連接mysql的套件
(需要安裝 microsoft c++ build tools)

```
pip install mysqlclient
```
如果不能安裝，可以參考 https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient 去下載對應python及電腦版本的whl檔案，並使用pip安裝(記得在虛擬環境下)，這邊不贅述。

安裝好之後，進入mysite/settings.py底下，修改DATABASES設定


```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'momomywife',                       # Or path to database file if using sqlite3.
        'USER': 'root',                       # Not used with sqlite3.
        'PASSWORD': '9527',               # Not used with sqlite3.
        'HOST': '140.119.19.167',                           # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                           # Set to empty string for default. Not used with sqlite3.
    }
}
```

修改好後，可以下看看migration指令，如下:

```
python manage.py makemigrations
python manage.py migrate
```

如果報錯代碼是2059，可參考 https://blog.csdn.net/weekdawn/article/details/81039382
解決密碼加密的問題。

## 4. 啟動django專案

在確認資料庫和app都設定好之後，我們就可以啟動專案了!
利用manage.py啟動:

```
python manage.py runserver
```
啟動後會開啟127.0.0.1:8000的網站，看到congratulations就代表設定成功了~



