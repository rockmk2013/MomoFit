from django.urls import path
from . import views
from momofit.views import Hello_momo

urlpatterns = [
    path('user/', views.Hello_momo, name='user_page'),
]