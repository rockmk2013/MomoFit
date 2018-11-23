from django.shortcuts import render
# Create your views here.
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.views import generic


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def Hello_momo(request):
    if request.user.is_authenticated:
        print(request.user.kcal)
        context = {
            "name": request.user.username,
            "age": request.user.age,
            "sex": request.user.sex,
            "height": request.user.height,
            "weight": request.user.weight,
            "kcal": request.user.kcal
        }
    return render(request, 'profile.html', context=context)