from django.urls import path
from django.views.generic import RedirectView
from . import views
from momofit.views import Hello_momo


urlpatterns = [
    path('profile/', views.Hello_momo, name='profile'),
    # path('signup/', views.SignUp.as_view(), name='signup'),
    path('signup/', views.SignUp, name='signup'),
    path('menu/',views.Menu,name='menu'),
    path('train_record/', views.Train_record, name="train_record"),
    path('food_record/', views.Food_record, name='food_record')
]