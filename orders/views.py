from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm

def login(request):
    context = {'form': AuthenticationForm()}
    return render(request, 'orders/login.html', context)

def under_construction(request, *args, **kwargs):
    return render(request, 'orders/under_construction.html')

def index(request):
    context = {
        # Здесь можно добавить данные, которые будут переданы в шаблон
    }
    return render(request, 'orders/index.html', context)