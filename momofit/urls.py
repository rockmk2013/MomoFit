from django.urls import path
from django.views.generic import RedirectView
from . import views
from momofit.views import Hello_momo


urlpatterns = [
    path('profile/', views.Hello_momo, name='profile'),
    # path('signup/', views.SignUp.as_view(), name='signup'),
    path('signup/', views.SignUp, name='signup'),
]