from django.shortcuts import render
from django.http import HttpResponse 
# Create your views here.

def Hello_momo(request):
    return HttpResponse("Hello Momo!")