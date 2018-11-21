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

    context = {
        "hihi":"yoyo"
    }
    return render(request, 'profile.html', context=context)