from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'orders/login.html', {'form': form})


def under_construction(request, *args, **kwargs):
    return render(request, 'orders/under_construction.html')

def index(request):
    context = {
        # Здесь можно добавить данные, которые будут переданы в шаблон
    }
    return render(request, 'orders/index.html', context)